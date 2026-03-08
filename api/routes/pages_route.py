import fastapi
from fastapi import Request
from fastapi.templating import Jinja2Templates

router = fastapi.APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(
        name="home.html",
        context={"request": request}
    )


@router.get("/chat")
async def chat_model(request: Request):
    return templates.TemplateResponse(
        name="chat.html",
        context={"request": request}
    )

@router.get("/web")
async def web_page(request: Request):
    return templates.TemplateResponse(
        name="web.html",
        context={"request": request}
    )

