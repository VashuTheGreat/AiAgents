import fastapi
from src.MultiRag.graph.builder import load_conversation
import logging

router = fastapi.APIRouter()

@router.get("/load_conversation")
async def get_conversation(thread_id: str):
    try:
        logging.info(f"Loading conversation for thread_id: {thread_id}")
        messages = await load_conversation(thread_id)
        logging.info(f"Conversation loaded successfully for thread_id: {thread_id}")
        return {"messages": messages}
    except Exception as e:
        logging.error(f"Error loading conversation for thread_id: {thread_id}: {e}")
        return {"message": "Failed to load conversation"}
    