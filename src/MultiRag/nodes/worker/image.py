import logging
from utils.asyncHandler import asyncHandler
from src.MultiRag.models.worker_model import State

@asyncHandler
async def image_node(state: State) -> State:
    file_path = state.file_path

    result = """
    Extracted Text from Image:

    "Artificial Intelligence is the new electricity."
    - Andrew Ng

    Diagram Description:
    The image shows a pipeline:
    Data → Preprocessing → Model → Evaluation → Deployment

    Labels:
    - Input Data
    - Training Phase
    - Model Accuracy Graph

    Interpretation:
    The image represents a standard ML workflow pipeline.
    """

    state.analysis_result = result
    return state