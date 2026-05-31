from src.graphs.builder import graph
from utils.asyncHandler import asyncHandler
import logging

class RunGraph:
    def __init__(self):
        pass

    @asyncHandler
    async def run(self, state: dict) -> dict:
        logging.info("Starting RunGraph component execution...")
        result = await graph.ainvoke(state)
        logging.info("RunGraph component execution completed.")
        return result