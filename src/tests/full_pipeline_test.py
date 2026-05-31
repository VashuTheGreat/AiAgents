import os
import sys
import logging
import asyncio
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.join(os.getcwd(), "src"))
sys.path.insert(0, os.getcwd())
import logger

from entity.config_entity import (
    DataIngestionConfig, 
    ContentEmbedderConfig, 
    DataTransformationConfig, 
    ContentTransformationConfig
)
from pipeline.DataIngestion_pipeline import DataIngestionPipeline
from pipeline.DataTransformation_pipeline import DataTransformationPipeline
from pipeline.GraphRunner_pipeline import RunGraphPipeline
from langchain_core.messages import HumanMessage

async def main():
    logging.info("Starting Full Pipeline Integration Test...")
    
    ingestion_configs = [
        DataIngestionConfig(input_file_path="/home/vashuthegreat/Projects/Multi-Rag/data/growing_ai_tools.txt"),
        DataIngestionConfig(input_file_path="/home/vashuthegreat/Projects/Multi-Rag/data/lena.png")
    ]
    content_embedder_config = ContentEmbedderConfig(data_ingestion_configs=ingestion_configs)
    
    ingestion_pipeline = DataIngestionPipeline(content_embedder_config=content_embedder_config)
    ingestion_result = await ingestion_pipeline.run_pipeline()
    logging.info(f"Ingestion Result: {ingestion_result}")

    transformation_configs = []
    for artifact in ingestion_result.data_ingestion_artifacts:
        base_run_dir = os.path.dirname(os.path.dirname(artifact.ingested_file_path))
        file_uuid = os.path.splitext(os.path.basename(artifact.ingested_file_path))[0]
        unique_path = os.path.join(base_run_dir, "transformation", "vector_store", file_uuid)
        transformation_configs.append(DataTransformationConfig(vector_store_path=unique_path))
    
    content_transformation_config = ContentTransformationConfig(data_transformation_configs=transformation_configs)
    
    transformation_pipeline = DataTransformationPipeline(
        content_transformation_config=content_transformation_config,
        content_embedder_artifact=ingestion_result
    )
    transformation_result = await transformation_pipeline.run_pipeline()
    
    logging.info(f"Transformation Result: {transformation_result}")
    logging.info(f"Total Transformation Artifacts: {len(transformation_result.data_transformation_artifacts)}")

    vector_store_paths = [art.vector_store_path for art in transformation_result.data_transformation_artifacts]
    
    initial_state = {
        "messages": [HumanMessage(content="What is growing AI tools?")],
        "vector_store_file_paths": vector_store_paths
    }
    
    graph_pipeline = RunGraphPipeline()
    graph_result = await graph_pipeline.run_graph(state=initial_state)
    logging.info(f"Graph execution result: {graph_result}")

asyncio.run(main=main())