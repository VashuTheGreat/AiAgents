import logging
import sys
from src.Blog.models.Task_models import Task
from src.Blog.models.Plan_model import Plan
from src.Blog.models.Evidence_model import EvidenceItem
from src.Blog.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from src.Blog.prompts import WORKER_SYSTEM
from exception import MyException
from utils.asyncHandler import asyncHandler


@asyncHandler
async def worker_node(payload: dict) -> dict:
    logging.info("Entering worker_node")
    try:
        task = Task(**payload["task"])
        plan = Plan(**payload["plan"])
        evidence = [EvidenceItem(**e) for e in payload.get("evidence", [])]
        topic = payload["topic"]
        mode = payload.get("mode", "closed_book")

        logging.debug(f"Task: {task.title}, Mode: {mode}")

        bullets_text = "\n- " + "\n- ".join(task.bullets)

        evidence_text = ""
        if evidence:
            evidence_text = "\n".join(
                f"- {e.title} | {e.url} | {e.published_at or 'date:unknown'}".strip()
                for e in evidence[:20]
            )

        response = await llm.ainvoke(
            [
                SystemMessage(content=WORKER_SYSTEM),
                HumanMessage(
                    content=(
                        f"Blog title: {plan.blog_title}\n"
                        f"Audience: {plan.audience}\n"
                        f"Tone: {plan.tone}\n"
                        f"Blog kind: {plan.blog_kind}\n"
                        f"Constraints: {plan.constraints}\n"
                        f"Topic: {topic}\n"
                        f"Mode: {mode}\n\n"
                        f"Section title: {task.title}\n"
                        f"Goal: {task.goal}\n"
                        f"Target words: {task.target_words}\n"
                        f"Tags: {task.tags}\n"
                        f"requires_research: {task.requires_research}\n"
                        f"requires_citations: {task.requires_citations}\n"
                        f"requires_code: {task.requires_code}\n"
                        f"Bullets:{bullets_text}\n\n"
                        f"Evidence (ONLY use these URLs when citing):\n{evidence_text}\n"
                    )
                ),
            ]
        )
        section_md = response.content.strip()

        logging.info(f"Worker node completed task: {task.title}")
        return {"sections": [(task.id, section_md)]}
    except Exception as e:
        logging.error(f"Error in worker_node: {str(e)}")
        raise MyException(e, sys)