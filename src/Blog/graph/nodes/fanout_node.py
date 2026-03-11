import logging
from src.Blog.models.State_model import State
from langgraph.types import Send


def fanout(state: State):
    logging.info("Entering fanout")
    tasks = state["plan"].tasks
    logging.debug(f"Fanning out {len(tasks)} tasks")
    
    return [
        Send(
            "worker",
            {
                "task": task.model_dump(),
                "topic": state["topic"],
                "mode": state["mode"],
                "plan": state["plan"].model_dump(),
                "evidence": [e.model_dump() for e in state.get("evidence", [])],
            },
        )
        for task in tasks
    ]