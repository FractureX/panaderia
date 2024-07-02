import os
from fastapi import APIRouter, status
from fastapi.responses import FileResponse

from src.shared.models.response import messages
from src.shared.models.response.messages import getDataNotFound
from src.shared.models.response.response import (
    getJsonResponse
)
from src.shared.utils.auths_per_user import Module

router = APIRouter()

# Lista de directorios permitidos
ALLOWED_DIRECTORIES = [f"images/{module.value}" for module in Module]

# Crear los directorios si no existen
for directory in ALLOWED_DIRECTORIES:
    os.makedirs(directory, exist_ok=True)

@router.get("/{directory}/{filename}")
async def get_image(directory: str, filename: str):
    if directory not in ALLOWED_DIRECTORIES:
        return getJsonResponse(status_code=status.HTTP_400_BAD_REQUEST, success=False, message=messages.IMAGE_DIRECTORY_NOT_FOUND, data={})
    file_location = os.path.join(directory, filename)
    if os.path.exists(file_location):
        return FileResponse(file_location)
    else:
        return getJsonResponse(status_code=status.HTTP_404_NOT_FOUND, success=False, message=getDataNotFound("Image"), data={})
