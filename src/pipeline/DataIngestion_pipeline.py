from components.data_ingestion import DataIngestion
from entity.config_entity import ContentEmbedderConfig
from entity.artifact_entity import ContentEmbedderArtifact, DataIngestionArtifact
from utils.asyncHandler import asyncHandler
import logging

class DataIngestionPipeline:
    def __init__(self, content_embedder_config: ContentEmbedderConfig):
        self.content_embedder_config = content_embedder_config

    @asyncHandler
    async def run_pipeline(self) -> ContentEmbedderArtifact:
        logging.info("Starting Data Ingestion Pipeline...")
        data_ingestion_artifacts = []

        for config in self.content_embedder_config.data_ingestion_configs:
            logging.info(f"Processing ingestion for: {config.input_file_path}")
            data_ingestion = DataIngestion(data_ingestion_config=config)
            artifact = await data_ingestion.ingest_data()
            data_ingestion_artifacts.append(artifact)
            logging.info(f"Ingestion completed for: {config.input_file_path}")

        logging.info("Data Ingestion Pipeline completed.")
        return ContentEmbedderArtifact(data_ingestion_artifacts=data_ingestion_artifacts)
