import logging
from langgraph.graph.message import MessagesState
from pydantic import BaseModel
from typing import List

class State(MessagesState):
    vector_store_file_paths: List[str]
    queries: List[str]
    retreived_results: List[str]
    ai_response: str

class Orchastrator_output(BaseModel):
    quetries: List[str]