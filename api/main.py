from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.routes import chat_route, uploader_route, pages_route
from api.routes.web import web_talk_routes
app = FastAPI()

@app.middleware("http")
async def check_user_id(request: Request, call_next):
    # Skip middleware for static files and page routes to allow initial connection
    public_routes = [
        "/",
        "/chat",
        "/web",
        "/docs",
        "/redoc",
        "/openapi.json"
    ]
    if request.url.path.startswith("/static") or request.url.path in public_routes:
        return await call_next(request)

    user_id = request.headers.get("user_id")

    if not user_id:
        return JSONResponse(
            status_code=401,
            content={"message": "user_id header missing"}
        )

    response = await call_next(request)
    return response

app.include_router(pages_route.router)
app.include_router(prefix="/chat", router=chat_route.router)
app.include_router(prefix="/uploader", router=uploader_route.router)

app.include_router(prefix="/web",router=web_talk_routes.router)


