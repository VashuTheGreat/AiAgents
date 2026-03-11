from typing import Literal, List
from pydantic import BaseModel, Field

class RouterDecision(BaseModel):
    needs_research: bool = Field(
        ...,
        description="Whether the topic requires external web research to provide an accurate and up-to-date answer. Use true or false."
    )
    mode: Literal["closed_book", "hybrid", "open_book"] = Field(
        ...,
        description="The mode of operation based on the knowledge requirement."
    )
    queries: List[str] = Field(
        default_factory=list,
        description="A list of 3-5 specific search queries if research is needed. Empty list otherwise."
    )