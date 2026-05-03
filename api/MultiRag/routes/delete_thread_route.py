import fastapi
import logging
import os
import shutil
from exception import MyException
from api.constants import DATA_FOLDER_PATH,DB_FOLDER_PATH
from src.MultiRag.graph.builder import deleteThread
router = fastapi.APIRouter()


@router.delete("/delete_thread")
async def delete_thread(thread_id: str):
    try:
        logging.info(f"Attempting to delete thread {thread_id}")
        await deleteThread(thread_id)
        
        data_path = f"{DATA_FOLDER_PATH}/{thread_id}"
        db_path = f"{DB_FOLDER_PATH}/{thread_id}"
        
        if os.path.exists(data_path):
            shutil.rmtree(data_path)
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
            
        logging.info(f"Successfully deleted thread {thread_id}")
        return {"message": f"Thread {thread_id} has been deleted."}
    except Exception as e:
        logging.error(f"Failed to delete thread {thread_id}: {str(e)}")
        raise MyException("Failed to delete thread") from e