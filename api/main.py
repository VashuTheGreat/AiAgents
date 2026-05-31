from fastapi import FastAPI

app = FastAPI( 
    description="This is a MultiRag App",
    title="Multi-Rag App",
    version="0.0.1",
    )



@app.get("/")
async def hello():
    return {"Hello": True}

