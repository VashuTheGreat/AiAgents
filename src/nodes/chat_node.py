import logging
from src.models.rag_model import State
from src.utils.asyncHandler import asyncHandler
from src.llm.llm_loader import llm
from src.prompts.prompt_templates import CHAT_PROMPT
from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

@asyncHandler
async def chat(state:State):
    logging.info("Executing chat node...")
    
    # Format the prompt using state
    formatted_prompt = CHAT_PROMPT
    
    prompt=[
        SystemMessage(content=formatted_prompt),
        SystemMessage(content=f"summary of the user uploaded content keywords with weightage: {state['summary']}"),
        # Assuming retreiver_responses contains relevant documents
        HumanMessage(content=f"Context: {state.get('retreiver_responses', [])}\nuserQuery: {state['userQuery']}")
    ]
    
    logging.debug(f"Chat prompt: {prompt}")
    res = await (llm | StrOutputParser()).ainvoke(prompt)
    logging.info("Chat node execution completed.")
    return {"llm_response":res}

    