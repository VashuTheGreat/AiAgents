from pydantic import BaseModel
from typing import TypedDict, List, Any, Optional
from typing_extensions import Annotated
from langchain_core.messages import BaseMessage
import operator

class Content(BaseModel):
    name:str
    about:str
    path:str

from src.MultiRag.models.orchestrator_output_model import OrchestratorOutput

class State(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    userContent: List[Content]
    thread_id: str
    topic: Optional[str]
    mode: Optional[str]
    plan: Optional[OrchestratorOutput]
    evidence: Annotated[List[Any], operator.add]
    worker_result: Annotated[List[Any], operator.add]
