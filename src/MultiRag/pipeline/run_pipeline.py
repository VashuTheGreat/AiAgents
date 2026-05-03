from src.MultiRag.components.run_graph import RunComponent
from utils.asyncHandler import asyncHandler
from src.MultiRag.models.rag_model import State, Content
from langchain_core.messages import HumanMessage
import logging

class RunPipeline:
    def __init__(self):
        self.run_component=RunComponent()
        pass
    
    @asyncHandler
    async def initiate(self, thread_id: str, query: str, userContent: list[Content] = []):
        logging.info("Entered in the initiate method of runPipeline")
        logging.info(f"Thread ID: {thread_id}, Query: {query}, Files: {len(userContent)}")

        state: State = State(
            messages=[HumanMessage(content=query)],
            userContent=userContent,
            thread_id=thread_id,
            topic=None,
            mode=None,
            plan=None,
            evidence=[],
            worker_result=[]
        )
        logging.info("State initialized")

        res=await self.run_component.run(state=state, thread_id=thread_id)
        logging.info(f"Pipeline execution completed, result: {res}")

        return res

