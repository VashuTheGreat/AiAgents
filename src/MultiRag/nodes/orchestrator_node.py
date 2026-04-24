import logging
from utils.asyncHandler import asyncHandler

from src.MultiRag.models.rag_model import State
from src.MultiRag.models.orchestrator_output_model import OrchestratorOutput
from src.MultiRag.llm.llm_loader import llm
from src.MultiRag.prompts.prompt_templates import ORCHESTRATOR_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage

@asyncHandler
async def orchestrator_node(state:State):
    logging.info("Entered in the orchestrator_node")
    logging.info(f"Current messages: {len(state.get('messages', []))} message(s)")

    orchestrator_llm = llm.with_structured_output(OrchestratorOutput)
    
    user_content = state.get('userContent', [])
    files_info = "\n".join([f"- Name: {c.name}, Path: {c.path}, About: {c.about}" for c in user_content])
    logging.info(f"Files available for orchestration: {len(user_content)}")
    
    system_prompt = ORCHESTRATOR_PROMPT + f"\n\n### Available Files:\n{files_info}\n\nWhen using a worker, you MUST specify the exact 'file_path' and 'file_type' (one of: pdf, txt, docs, png, url) from the list above."
    
    prompt= [SystemMessage(content=system_prompt)]+ state.get('messages', [])
    logging.info("Invoking orchestrator LLM with file context...")
    response = await orchestrator_llm.ainvoke(prompt)
    logging.info(f"Orchestrator response: {response}")
    return {"plan": response}
