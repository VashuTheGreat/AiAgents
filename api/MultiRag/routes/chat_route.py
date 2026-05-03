from fastapi import APIRouter, Request, Query
import logging
import logging
from src.MultiRag.pipeline.run_pipeline import RunPipeline
from src.MultiRag.graph.builder import graph
from src.MultiRag.models.rag_model import Content
from api.MultiRag.controllers.loadUserContent_component import load_user_content
from exception import MyException

router = APIRouter()

run_pipeline = RunPipeline()
async def run_agent(user_id, thread_id, userQuery: str):
    logging.info(f"Starting AIAgents application for thread: {thread_id}")
     
    try:
        temp_user_content = await load_user_content(thread_id)
       

        res = await run_pipeline.initiate(
            thread_id=thread_id, 
            query=userQuery,
            userContent=temp_user_content
        )
        return res
    except Exception as e:
        logging.error(f"Application failed: {e}")
        raise MyException("AIAgents application failed") from e
    finally:
        logging.info("AIAgents application finished.")


@router.post("/chat")
async def chat(req: Request, message: str = Query(...)):
    try:
        user_id = req.headers.get("user_id")
        thread_id = req.headers.get("thread_id") or user_id
        if not user_id:
            return {"data": "User ID missing in headers"}
        res = await run_agent(user_id, thread_id, message)
        
        # Extract the last message content to send to frontend
        messages = res.get("messages", [])
        if messages:
            last_msg = messages[-1]
            content = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
            return {"data": content}
            
        return {"data": "No response from agent."}
    except Exception as e:
        logging.error(f"Chat endpoint error: {e}")
        return {"data": "Chat failed"}

          
