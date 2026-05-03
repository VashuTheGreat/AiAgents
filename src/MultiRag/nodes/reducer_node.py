import logging
from src.MultiRag.models.rag_model import State
from langchain_core.messages import HumanMessage
from utils.asyncHandler import asyncHandler

@asyncHandler
async def reducer_node(state: State):
    results = state.get("worker_result", [])
    
    file_content = []
    web_content = []
    
    for res in results:
        if hasattr(res, "page_content"):
            source = res.metadata.get("source", "Unknown")
            is_web = res.metadata.get("type") == "web"
            content = f"--- SOURCE: {source} ---\n{res.page_content}"
            if is_web:
                web_content.append(content)
            else:
                file_content.append(content)
        else:
            file_content.append(str(res))
            
    merged_context = ""
    if file_content:
        merged_context += "IMPORTANT CONTEXT FROM UPLOADED FILES:\n" + "\n\n".join(file_content) + "\n\n"
    if web_content:
        merged_context += "CONTEXT FROM WEB SEARCH:\n" + "\n\n".join(web_content) + "\n\n"

    logging.info(f"Reducer node merged {len(results)} results.")
    
    context_msg = HumanMessage(content=f"{merged_context}Use the above information to answer the user's request.")
    return {"messages": [context_msg]}