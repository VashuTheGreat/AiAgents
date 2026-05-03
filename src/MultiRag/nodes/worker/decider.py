
from utils.asyncHandler import asyncHandler
from src.MultiRag.models.worker_model import State
import logging
from src.MultiRag.constants import AVAILABLE_ANALYSIS


@asyncHandler
async def decider_node(state:State):
    
    if state.file_type in AVAILABLE_ANALYSIS:
        return state.file_type
    
    else:
        return "end"
