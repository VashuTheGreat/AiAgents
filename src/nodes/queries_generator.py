import logging
from src.models.rag_model import State
from src.utils.asyncHandler import asyncHandler
from src.llm.llm_loader import llm
from src.models.queries_model import Queries
from src.prompts.prompt_templates import QUERY_GENERATION_PROMPT

from langchain_core.messages import SystemMessage, HumanMessage

@asyncHandler
async def query_generator(state:State):
    logging.info("Generating queries...")
    llm_=llm.with_structured_output(Queries)
    
    # Format the template into a string
    system_content = QUERY_GENERATION_PROMPT
    
    prompt=[
        SystemMessage(content=system_content),
        SystemMessage(content=f"summary of the user uploaded content keywords with weightage: {state['summary']}"),
        HumanMessage(content=f"userQuery: {state['userQuery']}")
    ]
    logging.debug(f"Query generator prompt: {prompt}")
    res = await llm_.ainvoke(prompt)
    logging.info(f"Generated {len(res.queries)} queries.")
    responses=[]
    for r in res.queries:
        logging.debug(f"Invoking retriever for query: {r}")
        responses.append(await state['retreiver'].invoke(r))

    logging.info("Query generation and retrieval completed.")
    return {"retreiver_responses":responses,"queries":res.queries}    


    

