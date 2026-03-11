from pydantic import BaseModel
class BlogDeleteRequest(BaseModel):
    data: dict