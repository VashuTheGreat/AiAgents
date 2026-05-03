import logging
import json
import re
from src.MultiRag.models.rag_model import State
from utils.asyncHandler import asyncHandler
from src.MultiRag.llm.llm_loader import llm
from src.MultiRag.prompts.prompt_templates import CHAT_PROMPT
from langchain_core.messages import SystemMessage, AIMessage
from src.MultiRag.tools.web_search import WebSearch

web_search_tool = WebSearch().search



@asyncHandler
async def chat_node(state: State):
    logging.info("Executing chat node...")
    tool_limit_hit = state.get("jump_to") == "end"
    has_context = len(state.get("worker_result", [])) > 0 or len(state.get("evidence", [])) > 0

    is_greeting = False
    if not has_context and len(state.get('messages', [])) > 0:
        last_human_msg = state.get('messages')[-1].content.lower()
        if last_human_msg in ["hi", "hello", "hey", "how are you", "who are you"]:
            is_greeting = True

    if tool_limit_hit or has_context or is_greeting:
        if has_context:
            logging.info("Context found from workers. Disabling web search to prevent redundant searches.")
        elif is_greeting:
            logging.info("Greeting detected. Disabling tools for natural conversation.")
        else:
            logging.info("Tool call limit hit. Invoking LLM without tools.")
        chat_llm = llm
    else:
        logging.info("Binding chat LLM with web search tool (limit check enabled)")
        chat_llm = llm.bind_tools([web_search_tool])
    prompt = [
        SystemMessage(content=CHAT_PROMPT + "\nIMPORTANT: Do NOT write JSON tool calls manually. If you want to use a tool, use the native tool-calling function. If you are just chatting or greeting, respond only in plain, friendly Markdown text.")
    ] + state.get('messages', [])
    
    if prompt:
        last_msg = prompt[-1]
        logging.info(f"Last message in prompt: {last_msg.content[:200]}...")

    logging.info("Invoking chat LLM...")
    res = await chat_llm.ainvoke(prompt)
  

    logging.info(f"Response retrieved from chat_llm: {res.content if res.content else 'Tool Call'}")
    return {"messages": [res]}
