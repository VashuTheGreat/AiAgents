import logging
from src.MultiRag.models.rag_model import State
from utils.asyncHandler import asyncHandler
from src.MultiRag.llm.llm_loader import llm
from src.MultiRag.prompts.prompt_templates import CHAT_PROMPT
from langchain_core.messages import SystemMessage

@asyncHandler
async def chat_node(state: State):
    logging.info("Executing chat node...")
    prompt = [SystemMessage(content=CHAT_PROMPT)] + state.get('messages', [])
    logging.info("Invoking chat LLM...")
    res = await llm.ainvoke(prompt)
    logging.info(f"Response retrieved from chat_llm: {res.content if hasattr(res, 'content') else res}")
    return {"messages": [res]}
