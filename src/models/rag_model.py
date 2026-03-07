from pydantic import BaseModel
from typing import TypedDict, List, Any
from typing_extensions import Annotated
from langchain_core.messages import BaseMessage
import operator

class State(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    userQuery: str
    db_path: str
    docs_path: str
    llm_response: str
    k: int
    queries: List[str]
    retreiver: Any
    retreiver_responses: List[Any]
    retreiver_response: Any
    summary: str
