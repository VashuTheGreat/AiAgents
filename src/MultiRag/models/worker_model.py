from pydantic import BaseModel
from typing import Optional, Literal, Any

class State(BaseModel):
    plan_to_retrieve: str
    file_type: Literal['pdf', 'txt', 'docs', 'png', 'url']
    file_path: str
    analysis_result: Any # temp output