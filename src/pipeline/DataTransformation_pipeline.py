from components.data_transformation import DataTransformation
from entity.config_entity import ContentTransformationConfig
from entity.artifact_entity import ContentTransformedArtifact, ContentEmbedderArtifact
from utils.asyncHandler import asyncHandler
import logging

class DataTransformationPipeline:
    def __init__(self, content_transformation_config: ContentTransformationConfig, content_embedder_artifact: ContentEmbedderArtifact):
        self.content_transformation_config = content_transformation_config
        self.content_embedder_artifact = content_embedder_artifact

    @asyncHandler
    async def run_pipeline(self) -> ContentTransformedArtifact:
        logging.info("Starting Data Transformation Pipeline...")
        data_transformation_artifacts = []

        for config, ingestion_artifact in zip(
            self.content_transformation_config.data_transformation_configs,
            self.content_embedder_artifact.data_ingestion_artifacts
        ):
            logging.info(f"Transforming artifact: {ingestion_artifact.ingested_file_path}")
            data_transformation = DataTransformation(
                data_transformation_config=config,
                data_ingestion_artifact=ingestion_artifact
            )
            artifact = await data_transformation.initiate_data_transformation()
            data_transformation_artifacts.append(artifact)
            logging.info(f"Transformation completed for: {ingestion_artifact.ingested_file_path}")

        logging.info("Data Transformation Pipeline completed.")
        return ContentTransformedArtifact(data_transformation_artifacts=data_transformation_artifacts)
