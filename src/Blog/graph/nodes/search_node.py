import logging
import sys
import asyncio
import json
import re
from typing import List
from src.Blog.models.State_model import State
from src.Blog.components.taivily_search import Taivily_search
from exception import MyException
from src.Blog.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from src.Blog.prompts import RESEARCH_SYSTEM
from src.Blog.models.Evidence_model import EvidencePack, EvidenceItem
from utils.asyncHandler import asyncHandler


@asyncHandler
async def research_node(state: State) -> dict:
    logging.info("Entering research_node")
    try:
        taivily_search = Taivily_search()
        queries = state.get("queries", []) or []
        logging.debug(f"Queries for research: {queries}")
        max_results = 6

        raw_results: List[dict] = []

        for q in queries:
            logging.debug(f"Queuing tavily search for query: {q}")
            raw_results.extend(await taivily_search._tavily_search(q, max_results=max_results))
        
        if not raw_results:
            logging.warning("No raw results found during research")

            return {"evidence": []}

       

        logging.info(f"Extracted {len(raw_results)} raw results. Processing with LLM for EvidencePack.")
        
        try:
            extractor = llm.with_structured_output(EvidencePack)
            pack = await extractor.ainvoke(
                [
                    SystemMessage(content=RESEARCH_SYSTEM),
                    HumanMessage(content=f"Raw results:\n{raw_results}"),
                ]
            )
            if pack:
                logging.info(f"EvidencePack extracted (structured). Evidence count: {len(pack.evidence)}")
                dedup={}
                for e in pack.evidence:
                    dedup[e.url]=e
                return {"evidence": list(dedup.values())}
        except Exception as e:
            logging.warning(f"Structured output failed in research_node: {str(e)}. Attempting manual parse.")


    except Exception as e:
        logging.error(f"Error in research_node: {str(e)}")
        raise MyException(e, sys)
