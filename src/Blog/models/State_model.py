from pydantic import BaseModel,Field
from typing import List,Literal,TypedDict,Optional,Annotated
from src.Blog.models.Evidence_model import EvidenceItem
from src.Blog.models.Plan_model import Plan
import operator
class State(TypedDict):
    topic: str

    # routing / research
    mode: str
    needs_research: bool
    queries: List[str]
    evidence: List[EvidenceItem]
    plan: Optional[Plan]

    # workers
    sections: Annotated[List[tuple[int, str]], operator.add]  # (task_id, section_md)
    final: str