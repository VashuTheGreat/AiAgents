import uvicorn as uv
from api.main import app
from src.logger import *
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from src.constants import DATA_FOLDER_PATH,DB_FOLDER_PATH
import os
load_dotenv()
app.mount("/static", StaticFiles(directory="static"), name="static")

os.makedirs(DATA_FOLDER_PATH, exist_ok=True)
os.makedirs(DB_FOLDER_PATH, exist_ok=True)

if __name__ == "__main__":
    uv.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=["db/*", "data/*", "logs/*", "vector_db/*", ".venv/*"],
    )