import fastapi

import logging

router = fastapi.APIRouter()


@router.post("/analyse_url")
async def analyse_url(thread_id:str,url: str):
    try:
        
        if not url:
            return {"data": "URL missing in headers"}
        res = await run_agent(thread_id, url)
        return {"data": res}
    except Exception as e:
        logging.error(f"Chat endpoint error: {e}")
        return {"data": "Failed to chat"}