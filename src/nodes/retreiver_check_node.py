import logging
from src.models.rag_model import State
from src.utils.asyncHandler import asyncHandler
from src.entity.ingestion_config import IngestionConfig
from src.ingestion.ingest_pipeline import Ingestion
from src.retrievers.retriever import Retreiver
import os

@asyncHandler
async def retreiver_check(state:State):
    logging.info("Checking retriever status...")
    if not state.get('retreiver'):
        logging.info("Retriever not found in state. Initializing...")
        db_path=state['db_path']
        docs_path=state['docs_path']
        
        # Do not create db_path here; create_vector_store needs to know if it's new
        if not os.path.exists(docs_path):
            logging.info(f"Creating documents directory: {docs_path}")
            os.makedirs(docs_path, exist_ok=True)    

        ingestion_config=IngestionConfig(
            db_path=db_path,
            docs_path=docs_path
        )
        logging.info("Starting ingestion pipeline...")
        ingestion=Ingestion(ingestion_config=ingestion_config)

        ingestion_artifact=await ingestion.ingest_data()

        logging.info("Initializing retriever with ingestion artifacts...")
        retreiver=Retreiver(vector_db=ingestion_artifact.vector_db,k=state['k'])

        await retreiver.initiate_retreiver()
        logging.info("Retriever initialized successfully.")
        return {"retreiver":retreiver}
    
    logging.info("Retriever already exists in state.")
    return state





            
