import logging
import os
from src.Blog.models.ImageSpec_model import State, GlobalImagePlan
from utils.asyncHandler import asyncHandler
from langchain.messages import SystemMessage, HumanMessage
from src.Blog.prompts import IMAGE_PLACEHOLDER_GENERATION
from exception import MyException
import sys
from src.Blog.components.image_generation import ImageGeneration
from src.Blog.llm import image_planner_llm


@asyncHandler
async def reducer_sub_llm(state: State) -> State:
    logging.info("Calling Claude Haiku for image placeholder planning (structured output)")
    output = await image_planner_llm.with_structured_output(GlobalImagePlan).ainvoke(
        [
            SystemMessage(content=IMAGE_PLACEHOLDER_GENERATION),
            HumanMessage(content=state["prompt_markdown"]),
        ]
    )
    if not output:
        logging.error("LLM failed to return a valid image placeholder plan (output is None)")
        raise MyException("Failed to generate image placeholder plan from LLM", sys)

    state["output"] = output
    logging.info("Successfully generated image placeholder plan")
    return state


@asyncHandler
async def reducer_sub_image(state: State) -> State:
    output = state['output']
    image_generator = ImageGeneration()
    if not output:
        raise MyException("output from reducer_sub not found", sys)

    os.makedirs("images", exist_ok=True)

    logging.info(f"Starting image generation for {len(output.images)} images")
    for image_con in output.images:
        logging.debug(f"Generating image: {image_con.filename} with prompt: {image_con.prompt[:50]}...")
        image = await image_generator.generateImage(prompt=image_con.prompt)
        image.save(image_con.filename)
    logging.info("All images generated successfully")
    return state


@asyncHandler
async def merge_images_and_md(state: State) -> State:
    output = state["output"]
    md = output.md_with_placeholders

    logging.info(f"Merging {len(output.images)} images into Markdown")
    for im in output.images:
        alt_text = (
            im.filename.split("/")[-1]
            .replace(".png", "")
            .replace("_", " ")
        )
        md_image_tag = f"![{alt_text}](../{im.filename})"
        md = md.replace(im.placeholder, md_image_tag)

    state["final_md"] = md
    logging.info("Markdown merging completed")
    return state
