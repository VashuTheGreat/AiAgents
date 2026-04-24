import logging
from src.MultiRag.models.rag_model import State
from langchain_core.messages import HumanMessage
from utils.asyncHandler import asyncHandler

@asyncHandler
async def reducer_node(state: State):
    results = state.get("worker_result", [])
    merged_content = "\n\n".join([str(res) for res in results])
    logging.info(f"Reducer node merged {len(results)} worker result(s)")
    return {"messages": [HumanMessage(content=f"Context retrieved from files:\n{merged_content}\n\nPlease use this information to answer my previous question.")]}