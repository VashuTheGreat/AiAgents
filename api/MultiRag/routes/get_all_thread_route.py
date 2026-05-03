from src.MultiRag.graph.builder import retrieve_all_threads
import fastapi
import logging

router = fastapi.APIRouter()

@router.get("/get_all_thread")
async def get_all_thread():
    try:
        logging.info("Received request to get all threads")
        threads = await retrieve_all_threads()
        logging.info(f"Retrieved all threads successfully {threads}")
        return {"threads": threads}
    except Exception as e:
        logging.error(f"Error retrieving threads: {e}")
        return {"message": "Failed to retrieve threads"}
