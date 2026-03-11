import os
import fastapi
from fastapi import Request
from fastapi.templating import Jinja2Templates

router = fastapi.APIRouter()
templates = Jinja2Templates(directory="templates")

_APP_USER_ID = os.getenv("APP_API_KEY", "")

@router.get("/web")
async def web_page(request: Request):
    return templates.TemplateResponse(
        name="web.html",
        context={"request": request, "app_user_id": _APP_USER_ID}
    )
