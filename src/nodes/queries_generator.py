import logging
from src.models.rag_model import State
from src.utils.asyncHandler import asyncHandler
from src.llm.llm_loader import llm
from src.models.queries_model import Queries
from src.prompts.prompt_templates import QUERY_GENERATION_PROMPT
from src.nodes.retreiver_check_node import get_cached_retriever

from langchain_core.messages import SystemMessage, HumanMessage

@asyncHandler
async def query_generator(state: State):
    logging.info("Generating queries...")
    llm_ = llm.with_structured_output(Queries)

    system_content = QUERY_GENERATION_PROMPT

    prompt = [
        SystemMessage(content=system_content),
        SystemMessage(content=f"summary of the user uploaded content keywords with weightage: {state['summary']}"),
        HumanMessage(content=f"userQuery: {state['userQuery']}")
    ]
    logging.debug(f"Query generator prompt: {prompt}")
    res = await llm_.ainvoke(prompt)
    logging.info(f"Generated {len(res.queries)} queries.")

    # Fetch retriever from server-side cache (keyed by db_path, NOT stored in state)
    retreiver = get_cached_retriever(state['db_path'])
    if retreiver is None:
        logging.error(f"Retriever not found in cache for db_path={state['db_path']}")
        return {"retreiver_responses": [], "queries": res.queries}

    responses = []
    for r in res.queries:
        logging.info(f"Invoking retriever with query: {r}")
        responses.append(await retreiver.invoke(r))

    logging.info("Query generation and retrieval completed.")
    return {"retreiver_responses": responses, "queries": res.queries}
