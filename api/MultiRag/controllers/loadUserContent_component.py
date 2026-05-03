
from utils.asyncHandler import asyncHandler
from utils.main_utils import load_yaml
from api.constants import DATA_FOLDER_PATH,USER_CONTENT_FILE_NAME
from src.MultiRag.models.rag_model import Content

@asyncHandler
async def load_user_content(thread_id):
    user_data = load_yaml(f"{DATA_FOLDER_PATH}/{thread_id}/{USER_CONTENT_FILE_NAME}")
    user_content = []
    if user_data:
        for content in user_data.get("Contents", []):
            user_content.append(
                Content(
                    name=content["name"],
                    about=content["about"],
                    path=content["path"]
                )
            )

    return user_content