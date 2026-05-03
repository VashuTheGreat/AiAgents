

import fastapi
from api.constants import AVAILABLE_ANALYSIS
router = fastapi.APIRouter()


@router.get("/")
async def get_available_file_fomates():
    return {"message": "Available file formats: pdf, txt, docx, image","data":AVAILABLE_ANALYSIS}