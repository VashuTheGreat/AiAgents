import logging
import sys
import json
import re
from src.Blog.models.RouterDecision_model import RouterDecision
from langchain_core.messages import SystemMessage, HumanMessage
from src.Blog.models.State_model import State
from src.Blog.llm import llm
from src.Blog.prompts import ROUTER_SYSTEM
from exception import MyException
from utils.asyncHandler import asyncHandler


@asyncHandler
async def router_node(state: State):
    logging.info("Entering router_node")
    topic = state['topic']
    logging.debug(f"Topic: {topic}")
    
    try:
        try:
            runnable = llm.with_structured_output(RouterDecision)
            decision = await runnable.ainvoke(
                [
                    SystemMessage(content=ROUTER_SYSTEM),
                    HumanMessage(content=f"Topic: {topic}")
                ]
            )
            if decision:
                logging.info(f"Router decision (structured): needs_research={decision.needs_research}, mode={decision.mode}")
                return {
                    "needs_research": decision.needs_research,
                    "mode": decision.mode,
                    "queries": decision.queries,
                }
        except Exception as e:
            logging.warning(f"Structured output failed: {str(e)}. Attempting manual parse.")

        raw_response = await llm.ainvoke(
            [
                SystemMessage(content=ROUTER_SYSTEM + "\n\nCRITICAL: You MUST return a valid JSON object. Do not include any text before or after the JSON."),
                HumanMessage(content=f"Topic: {topic}")
            ]
        )
        content = raw_response.content
        logging.debug(f"Raw LLM content for fallback: {content}")

        json_str = ""
        markdown_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if markdown_match:
            json_str = markdown_match.group(1)
        else:
            start = content.find('{')
            end = content.rfind('}')
            if start != -1 and end != -1:
                json_str = content[start:end+1]
        
        if json_str:
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError:
                # Progressive truncation fallback
                success = False
                temp_str = json_str
                while '}' in temp_str:
                    try:
                        data = json.loads(temp_str)
                        success = True
                        break
                    except json.JSONDecodeError:
                        last_brace = temp_str.rfind('}')
                        if last_brace == -1: break
                        temp_str = temp_str[:last_brace]
                
                if not success:
                    raise ValueError("Failed to parse JSON even after structural truncation")

            needs_res = str(data.get("needs_research", "")).lower() in ["true", "1", "yes"]
            
            decision = RouterDecision(
                needs_research=needs_res,
                mode=data.get("mode", "open_book"),
                queries=data.get("queries", [])
            )
            logging.info(f"Router decision (manual): needs_research={decision.needs_research}, mode={decision.mode}")
            return {
                "needs_research": decision.needs_research,
                "mode": decision.mode,
                "queries": decision.queries,
            }

        logging.error("Failed to extract JSON from LLM response")
        raise ValueError("LLM failed to return a valid RouterDecision. Please check prompts or model output.")

    except Exception as e:
        logging.error(f"Error in router_node: {str(e)}")
        raise

def route_next(state: State) -> str:
    needs_research = state.get("needs_research", False)
    logging.info(f"Routing next based on research need: {needs_research}")
    return "research" if needs_research else "orchestrator"