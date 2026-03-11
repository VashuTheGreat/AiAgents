import re
import os
import sys
import logging
import zipfile
import io
from fastapi import  HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import  StreamingResponse
from fastapi.staticfiles import StaticFiles
from api.Blog.models.models import BlogDeleteRequest
import fastapi
import uvicorn as uv

PROJECT_ROOT = os.getcwd()
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from logger import *
from src.Blog.graph.Compile_graph import run
from src.Blog.utils.blog_utils import delete_blog_content

router=fastapi.APIRouter()
os.makedirs("images", exist_ok=True)
os.makedirs("results", exist_ok=True)

# Mount static files
router.mount("/images", StaticFiles(directory="images"), name="images")
router.mount("/results", StaticFiles(directory="results"), name="results")





@router.get("/blogs")
async def list_blogs():
    results_dir = "results"
    if not os.path.exists(results_dir):
        return []
    blogs = [f[:-3] for f in os.listdir(results_dir) if f.endswith(".md") and f != "README.md"]
    return blogs

@router.get("/blog/{title}")
async def get_blog(title: str):
    file_path = os.path.join("results", f"{title}.md")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Blog not found")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"title": title, "content": content}

from fastapi.encoders import jsonable_encoder

@router.websocket("/ws/generate_blog")
async def generate_blog_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        topic = data.get("topic")
        if not topic:
            await websocket.send_json({"error": "Topic is required"})
            await websocket.close()
            return

        logging.info(f"WebSocket: Starting blog generation for topic: {topic}")
        
        async for step in run(topic):
            serializable_step = jsonable_encoder(step)
            await websocket.send_json(serializable_step)
            
        await websocket.send_json({"status": "completed"})
    except WebSocketDisconnect:
        logging.info("WebSocket disconnected")
    except Exception as e:
        logging.error(f"WebSocket error: {str(e)}")
        await websocket.send_json({"error": str(e)})
    finally:
        try:
            await websocket.close()
        except:
            pass

@router.delete("/delete_blog")
async def delete_blog(request: BlogDeleteRequest):
    success = delete_blog_content(request.data)
    if success:
        return {"message": "Blog and associated images deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Blog not found or could not be deleted")

@router.get("/download_blog/{title}")
async def download_blog(title: str):
    md_path = os.path.join("results", f"{title}.md")
    if not os.path.exists(md_path):
        raise HTTPException(status_code=404, detail="Blog not found")

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find images
    image_pattern = r"!\[.*?\]\(\.\./images/(.*?)\)"
    image_filenames = re.findall(image_pattern, content)

    # Create zip in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        # Add markdown file
        zip_file.writestr(f"{title}.md", content)
        
        # Add images
        for img_name in image_filenames:
            img_path = os.path.join("images", img_name)
            if os.path.exists(img_path):
                zip_file.write(img_path, os.path.join("images", img_name))

    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename={title}.zip"}
    )

if __name__ == "__main__":
    uv.run("app:app", host="0.0.0.0", port=8000, reload=False)