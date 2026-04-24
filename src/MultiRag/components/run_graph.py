from src.MultiRag.graph.builder import graph
from utils.asyncHandler import asyncHandler
from src.MultiRag.models.rag_model import State

import logging

class RunComponent:
    def __init__(self):
        pass
    

    @asyncHandler
    async def run(self,state:State, thread_id:str):
        logging.info("Entered in the run_component")
        logging.info(f"Running graph with thread_id: {thread_id}")

        config = {"configurable": {"thread_id": thread_id}}
        res=await graph.ainvoke(state, config)
        logging.info(f"Graph execution completed")
        return res
