import os
import sys
import asyncio
sys.path.append(os.getcwd())

from dotenv import load_dotenv
load_dotenv()
from logger import *
import logging

from src.MultiRag.pipeline.run_pipeline import RunPipeline


from src.MultiRag.models.rag_model import Content

async def main():
    run_pipeline = RunPipeline()
    
    # Mocking user uploaded files
    temp_user_content = [
        Content(
            name="AI_Intro.pdf",
            about="An introductory document about Artificial Intelligence and Machine Learning.",
            path="/home/vashuthegreat/Projects/Multi-Rag/data/AI_Intro.pdf"
        ),
        Content(
            name="Notes.txt",
            about="General notes about software engineering.",
            path="/home/vashuthegreat/Projects/Multi-Rag/data/Notes.txt"
        )
    ]

    res = await run_pipeline.initiate(
        thread_id="2", 
        query="What does the AI_Intro.pdf say about Neural Networks?",
        userContent=temp_user_content
    )

    logging.info(f"Final Pipeline Response: {res}")



asyncio.run(main())