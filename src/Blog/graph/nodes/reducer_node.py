import logging
import sys
from pathlib import Path
from src.Blog.models.State_model import State
from exception import MyException
from utils.asyncHandler import asyncHandler
from src.Blog.constants import FOLDER_PATH_TO_SAVE_MD
import os
from src.Blog.graph.graphs.reducer_subgraph import app
@asyncHandler
async def reducer_node(state: State) -> dict:
    logging.info("Entering reducer_node")
    try:
        plan = state["plan"]

        ordered_sections = [md for _, md in sorted(state["sections"], key=lambda x: x[0])]
        body = "\n\n".join(ordered_sections).strip()
        final_md = f"# {plan.blog_title}\n\n{body}\n"

        filename = f"{plan.blog_title}.md"
        logging.debug(f"Writing final blog to {filename}")

        logging.info("Starting image generation and merging via subgraph")
        red_f_ob=await app.ainvoke({"prompt_markdown":final_md})
        final_md=red_f_ob["final_md"]
        
        logging.debug(f"Final MD size after merging: {len(final_md)} characters")
        os.makedirs(FOLDER_PATH_TO_SAVE_MD,exist_ok=True)
        file_path=os.path.join(FOLDER_PATH_TO_SAVE_MD,filename)
        Path(file_path).write_text(final_md, encoding="utf-8")

        logging.info(f"Reducer node completed successfully, blog saved to {file_path}")
        return {"final": final_md}
    except Exception as e:
        logging.error(f"Error in reducer_node: {str(e)}")
        raise MyException(e, sys)