from fastapi import APIRouter, Request, Query
import asyncio
import logging
import src.logger
from src.graph.builder import graph

router = APIRouter()


async def run_agent(user_id, userQuery: str):
    logging.info("Starting AIAgents application...")
    # Sample initial state for testing
    config = {"configurable": {"thread_id": user_id}}
    initial_state = {
        "userQuery": userQuery,
        "db_path": f"db/{user_id}",
        "docs_path": f"data/{user_id}",
        "k": 3
    }
    try:
        response = await graph.ainvoke(initial_state, config=config)
        logging.debug(f"Graph response: {response}")
        logging.info("Graph invocation successful.")
        res = response.get("llm_response", "No response found.")
        return res
    except Exception as e:
        logging.error(f"Application failed: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return "Chat failed due to internal error"
    finally:
        logging.info("AIAgents application finished.")


@router.post("/chat")
async def chat(req: Request, message: str = Query(...)):
    try:
        user_id = req.headers.get("user_id")
        if not user_id:
            return {"data": "User ID missing in headers"}
        res = await run_agent(user_id, message)
        return {"data": res}
    except Exception as e:
        logging.error(f"Chat endpoint error: {e}")
        return {"data": "Chat failed"}
