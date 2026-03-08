from langchain_community.document_loaders import WebBaseLoader
from src.utils.asyncHandler import asyncHandler
from src.models.web.web_model import State
from src.llm.llm_loader import llm
from src.prompts.prompt_templates import WEB_SUMERISER_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
import logging
@asyncHandler
async def web_summ_node(state:State)->State:
    logging.info("Entered in the web_summ_node node")
    prompt=[
        SystemMessage(
            content=WEB_SUMERISER_PROMPT
        ),
        HumanMessage(
            content=state['page_content']
        )
    ]

    res=await (llm | StrOutputParser()).ainvoke(prompt)
    logging.info("Exited from the web_summ_node node")
    return {"llm_response":res}



