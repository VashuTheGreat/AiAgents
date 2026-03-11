import logging
import sys
from src.Blog.models.State_model import State
from src.Blog.llm import llm
from exception import MyException
from src.Blog.models.Plan_model import Plan
from src.Blog.prompts import ORCH_SYSTEM
from langchain_core.messages import SystemMessage, HumanMessage
from utils.asyncHandler import asyncHandler


@asyncHandler
async def orchestrator_node(state: State) -> dict:
    logging.info("Entering orchestrator_node")
    try:
        planner = llm.with_structured_output(Plan)

        evidence = state.get("evidence", [])
        mode = state.get("mode", "closed_book")
        logging.debug(f"Mode: {mode}, Evidence count: {len(evidence)}")

        plan = await planner.ainvoke(
            [
                SystemMessage(content=ORCH_SYSTEM),
                HumanMessage(
                    content=(
                        f"Topic: {state['topic']}\n"
                        f"Mode: {mode}\n\n"
                        f"Evidence (ONLY use for fresh claims; may be empty):\n"
                        f"{[e.model_dump() for e in evidence][:16]}"
                    )
                ),
            ]
        )

        logging.info(f"Orchestrator plan created: {plan.blog_title} with {len(plan.tasks)} tasks.")
        return {"plan": plan}
    except Exception as e:
        logging.error(f"Error in orchestrator_node: {str(e)}")
        raise MyException(e, sys)