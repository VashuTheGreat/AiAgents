from pydantic import BaseModel,Field
from typing import List,Literal,TypedDict
class ImageSpec(BaseModel):
    placeholder:str=Field(...,description="e.g. [[IMAGE_1]]")
    filename:str=Field(...,description="Save under images/, e.g. qkv_flow.png")
    prompt:str=Field(...,description="Prompt to send to the image model")
    size:Literal["1024x1024","1024x1536","1536x1024"]="1025x1024"
    quality: Literal["low", "medium", "high"] = "medium"


class GlobalImagePlan(BaseModel):
    md_with_placeholders:str
    images:List[ImageSpec]=Field(default_factory=list)



class State(TypedDict):
    prompt_markdown:str
    final_md:str
    output: GlobalImagePlan
