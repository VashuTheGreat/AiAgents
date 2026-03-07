import os
import sys
sys.path.append(os.getcwd())

from src.ingestion.ingest_pipeline import Ingestion
from src.entity.ingestion_config import IngestionConfig
from src.logger import *
from dotenv import load_dotenv
load_dotenv()
import os
import asyncio

db_path="db/vansh"
docs_path="data/vansh"

if not os.path.exists(db_path):
    os.makedirs(db_path,exist_ok=True)
if not os.path.exists(docs_path):
    os.makedirs(docs_path)    

ingestion_config=IngestionConfig(
    db_path=db_path,
    docs_path=docs_path
)
ingestion=Ingestion(ingestion_config=ingestion_config)

print(asyncio.run(ingestion.ingest_data()))