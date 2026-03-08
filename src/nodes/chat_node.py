import logging
from src.models.rag_model import State
from src.utils.asyncHandler import asyncHandler
from src.llm.llm_loader import llm
from src.prompts.prompt_templates import CHAT_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

@asyncHandler
async def chat(state: State):
    logging.info("Executing chat node...")

    # Build prompt: system instructions + retrieved context + conversation history + current query
    prompt = [
        SystemMessage(content=CHAT_PROMPT),
        SystemMessage(content=f"Summary/keywords of uploaded document: {state.get('summary', '')}"),
        SystemMessage(content=f"Retrieved context relevant to this query:\n{state.get('retreiver_responses', [])}"),
    ]

    # Inject prior conversation history for multi-turn memory
    prior_messages = state.get("messages", [])
    if prior_messages:
        prompt.extend(prior_messages)

    # Append current user query
    prompt.append(HumanMessage(content=state['userQuery']))

    logging.debug(f"Chat prompt: {prompt}")
    res = await (llm | StrOutputParser()).ainvoke(prompt)
    logging.info("Chat node execution completed.")

    # Append this turn to messages so history accumulates across calls
    return {
        "llm_response": res,
        "messages": [
            HumanMessage(content=state['userQuery']),
            AIMessage(content=res),
        ]
    }
