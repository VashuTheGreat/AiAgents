import os
import fastapi
from fastapi.templating import Jinja2Templates
from fastapi import Request

router = fastapi.APIRouter()
templates = Jinja2Templates(directory="templates")

_APP_USER_ID = os.getenv("APP_API_KEY", "")

@router.get("/blog")
async def blog_root(request: Request):
    return templates.TemplateResponse(
        name="blog.html",
        context={"request": request, "app_user_id": _APP_USER_ID}
    )