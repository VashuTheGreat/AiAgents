from typing import TypedDict, Optional

class State(TypedDict):
    url: str
    page_content: Optional[str]
    llm_response: Optional[str]
