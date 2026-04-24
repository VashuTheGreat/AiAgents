import logging
from utils.asyncHandler import asyncHandler
from src.MultiRag.models.worker_model import State

@asyncHandler
async def pdf_node(state: State) -> State:
    file_path = state.file_path

    result = """
    Title: Introduction to Artificial Intelligence and Machine Learning

    Chapter 1: Overview
    Artificial Intelligence (AI) is a branch of computer science that aims to create systems capable of performing tasks that normally require human intelligence. These tasks include reasoning, learning, perception, and decision-making. Machine Learning (ML), a subset of AI, focuses on enabling systems to learn from data and improve over time without explicit programming.

    Chapter 2: Types of Machine Learning
    1. Supervised Learning: Uses labeled datasets to train models. Examples include classification and regression tasks.
    2. Unsupervised Learning: Works with unlabeled data to find hidden patterns. Examples include clustering and dimensionality reduction.
    3. Reinforcement Learning: Involves agents that learn by interacting with an environment and receiving rewards or penalties.

    Chapter 3: Key Algorithms
    - Linear Regression
    - Logistic Regression
    - Decision Trees
    - Support Vector Machines
    - Neural Networks

    Chapter 4: Neural Networks
    Neural networks are inspired by the human brain. They consist of layers of interconnected nodes (neurons). Deep Learning is a subset of ML that uses multi-layered neural networks to model complex patterns.

    Chapter 5: Applications
    AI and ML are used in various domains such as healthcare, finance, autonomous vehicles, recommendation systems, and natural language processing.

    Summary:
    AI is transforming industries by enabling automation and intelligent decision-making. ML plays a critical role in making systems adaptive and data-driven.
    """

    state.analysis_result = result
    return state