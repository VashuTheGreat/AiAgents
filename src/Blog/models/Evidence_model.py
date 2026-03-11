from typing import Optional,List,Literal
from pydantic import BaseModel,Field
class EvidenceItem(BaseModel):
    title: str
    url: str
    published_at: Optional[str] = None  # keep if Tavily provides; DO NOT rely on it
    snippet: Optional[str] = None
    source: Optional[str] = None



class EvidencePack(BaseModel):
    evidence: List[EvidenceItem] = Field(default_factory=list)    