import fastapi
from fastapi import UploadFile, Request, BackgroundTasks
import os
import logging
from src.MultiRag.graph.builder import deleteThread
from utils.asyncHandler import asyncHandler
from utils.main_utils import write_yaml, load_yaml
from src.MultiRag.models.rag_model import Content
from src.MultiRag.components.content_embedder import ContentEmbedder
from src.MultiRag.entity.config_entity import ContentEmbedderConfig
from api.constants import DATA_FOLDER_PATH, USER_CONTENT_FILE_NAME
from src.MultiRag.graph.builder import graph
from langchain_core.messages import HumanMessage

router = fastapi.APIRouter()

async def generate_retreivers(thread_id: str):
    yaml_path = f"{DATA_FOLDER_PATH}/{thread_id}/{USER_CONTENT_FILE_NAME}"
    yaml_content = load_yaml(yaml_path)
    
    if not yaml_content or 'Contents' not in yaml_content:
        logging.warning(f"No contents found in {yaml_path}")
        return

    for content_dict in yaml_content['Contents']:
        name = content_dict.get("name")
        path = content_dict.get("path")
        
        logging.info(f"Processing content: {name}")
    
        content_embedder_config = ContentEmbedderConfig(
            file_path=path,
            vector_store_path=f"db/{thread_id}/{name}",
        )
        component = ContentEmbedder(content_embedder_config=content_embedder_config)
        retreiver = await component.embed_content()
        logging.info(f"Generated retreiver for {name}: {retreiver}")

@router.post("/")
async def post_content(
    req: Request,
    file: UploadFile
):
    try:
        user_id = req.headers.get("user_id")
        thread_id = req.headers.get("thread_id") or user_id
        if not user_id:
            return {"message": "User ID missing in headers"}

        folder = f"{DATA_FOLDER_PATH}/{thread_id}"
        os.makedirs(folder, exist_ok=True)

        saved_file_path = f"{folder}/{file.filename}"
        with open(saved_file_path, "wb") as f:
            f.write(await file.read())

        yaml_path = f"{folder}/{USER_CONTENT_FILE_NAME}"
        
        content_entry = {
            "name": file.filename,
            "about": file.filename,
            "path": saved_file_path
        }

        # Append to YAML
        write_yaml(yaml_path, {"Contents": [content_entry]}, mode="a")
        
        logging.info(f"File uploaded and entry added to YAML: {file.filename}")

        # Trigger retriever generation
        await generate_retreivers(thread_id)

        # Notify the AI about the upload in the thread history
        config = {"configurable": {"thread_id": thread_id}}
        notification = HumanMessage(content=f"[SYSTEM NOTIFICATION]: User has uploaded a new file: {file.filename}. Please keep this in mind for future queries.")
        await graph.aupdate_state(config, {"messages": [notification]})

        return {"message": "File uploaded successfully"}

    except Exception as e:
        logging.error(f"File upload failed: {e}")
        return {"message": f"File upload failed: {str(e)}"}

@router.post("/upload_url")
async def upload_url(req: Request, url: str):
    try:
        user_id = req.headers.get("user_id")
        thread_id = req.headers.get("thread_id") or user_id
        if not user_id:
            return {"message": "User ID missing in headers"}

        folder = f"{DATA_FOLDER_PATH}/{thread_id}"
        os.makedirs(folder, exist_ok=True)

        yaml_path = f"{folder}/{USER_CONTENT_FILE_NAME}"
        
        # Use a truncated URL for the name
        display_name = (url[:50] + '...') if len(url) > 50 else url
        
        content_entry = {
            "name": display_name,
            "about": url,
            "path": url
        }

        # Append to YAML
        write_yaml(yaml_path, {"Contents": [content_entry]}, mode="a")
        
        logging.info(f"URL entry added to YAML: {url}")

        # Trigger retriever generation (if the embedder supports URLs)
        await generate_retreivers(thread_id)

        # Notify the AI about the URL upload
        config = {"configurable": {"thread_id": thread_id}}
        notification = HumanMessage(content=f"[SYSTEM NOTIFICATION]: User has uploaded a new URL: {url}. Please keep this in mind for future queries.")
        await graph.aupdate_state(config, {"messages": [notification]})

        return {"message": "URL uploaded successfully"}

    except Exception as e:
        logging.error(f"URL upload failed: {e}")
        return {"message": f"URL upload failed: {str(e)}"}