import logging
from utils.asyncHandler import asyncHandler
from src.MultiRag.models.worker_model import State

@asyncHandler
async def txt_node(state: State) -> State:
    file_path = state.file_path

    result = """
    AIML Notes:

    - AI stands for Artificial Intelligence
    - ML is a subset of AI
    - Data is the backbone of Machine Learning
    - Models learn patterns from data
    - Overfitting occurs when model memorizes instead of generalizing
    - Underfitting occurs when model fails to capture patterns

    Important Concepts:
    - Training vs Testing
    - Bias vs Variance
    - Feature Engineering
    - Model Evaluation Metrics (Accuracy, Precision, Recall)

    Conclusion:
    Understanding fundamentals is important before moving to advanced topics like Deep Learning and MLOps.
    """

    state.analysis_result = result
    return state