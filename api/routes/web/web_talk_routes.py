import fastapi
from src.graph.web.builder import graph
router=fastapi.APIRouter()

@router.post("/web_summerizer")
async def web_sum(url:str):

    res=await graph.ainvoke({
        "url":url
    })
    print(res)

    return {"data": res.get("llm_response", "Error generating response")}
