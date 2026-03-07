import logging
from src.models.rag_model import State
from src.utils.ingestion_utils import get_documents
from src.utils.asyncHandler import asyncHandler
from src.llm.llm_loader import llm
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from src.constants import TOP_K_KEYWORDS
from keybert import KeyBERT

kw_model = KeyBERT()

doc = """
Deep learning uses neural networks with multiple layers.
CNNs are widely used for image recognition.
"""

keywords = kw_model.extract_keywords(doc, top_n=5)

@asyncHandler
async def content_summerizer(state: State):
    logging.info("Executing summarizer node...")
    
    if not state.get('summary'):
        logging.info("Summarizing content using LLM...")
        summary_content = await get_documents(state['docs_path'])
        summary_content=str(kw_model.extract_keywords(summary_content, top_n=TOP_K_KEYWORDS))
        if not summary_content.strip():
            logging.warning("No content found to summarize.")
            return {"summary": "No content available."}
        return {"summary": summary_content}
            
    logging.info("Summary already exists in state.")
    return state