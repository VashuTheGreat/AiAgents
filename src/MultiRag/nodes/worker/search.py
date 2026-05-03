import logging
from utils.asyncHandler import asyncHandler
from src.MultiRag.models.worker_model import State
from src.MultiRag.tools.web_search import WebSearch

@asyncHandler
async def search_node(state: State) -> State:
    logging.info("Starting Search worker node...")
    query = state.plan_to_retrieve
    logging.info(f"Searching for: {query}")
    
    search_tool = WebSearch().search
    results = await search_tool.ainvoke(query)
    
    logging.info(f"Search completed. Found {len(results) if isinstance(results, list) else 'some'} results.")
    
    from langchain_core.documents import Document
    
    docs = []
    if isinstance(results, list):
        for r in results:
            content = r.get('content', str(r))
            url = r.get('url', 'Web Search')
            docs.append(Document(page_content=content, metadata={"source": url, "type": "web"}))
    else:
        docs.append(Document(page_content=str(results), metadata={"source": "Web Search", "type": "web"}))

    return {"worker_result": docs}
