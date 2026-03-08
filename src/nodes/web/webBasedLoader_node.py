from langchain_community.document_loaders import WebBaseLoader
from src.utils.asyncHandler import asyncHandler
from src.models.web.web_model import State
import logging

@asyncHandler
async def load_web_content(state:State)->State:
    logging.info("Entered in the load_web_content node")
    url=state['url']
    loader=WebBaseLoader(url)
    docs = loader.load()
    page_content = docs[0].page_content

    if len(page_content.split()) > 2000:
        raise OverflowError(f"The content is too large for llm {len(page_content.split())}")

    logging.info("Exited from the load_web_content node")

    return {"page_content":page_content}



