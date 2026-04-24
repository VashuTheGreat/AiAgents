import logging
from utils.asyncHandler import asyncHandler
from src.MultiRag.models.worker_model import State

@asyncHandler
async def url_node(state: State) -> State:
    url = state.file_path

    result = f"""
    Web Page Content from: {url}

    Title: What is Artificial Intelligence and Machine Learning?

    Artificial Intelligence (AI) refers to the simulation of human intelligence in machines. These machines are programmed to think, learn, and adapt.

    Machine Learning (ML) is a subset of AI that focuses on building systems that learn from data. Instead of being explicitly programmed, ML models improve their performance as they are exposed to more data.

    Key Topics Covered:
    - Supervised vs Unsupervised Learning
    - Deep Learning and Neural Networks
    - Real-world applications like chatbots, recommendation systems, and self-driving cars

    Latest Trends:
    - Generative AI (e.g., large language models)
    - MLOps for production systems
    - Edge AI for real-time processing

    Conclusion:
    AI and ML are rapidly evolving fields with significant impact on technology and society.
    """

    state.analysis_result = result
    return state