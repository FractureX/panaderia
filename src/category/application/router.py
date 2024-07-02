from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from psycopg2.extensions import connection
from typing import Any

from src.category.infrastructure import service
from src.shared.models.response.response import (
    CustomResponses,
)
from src.shared.infrastructure.database.sqlserver import SQLServer
from src.auth.utils.functions.functions import validate_token

router = APIRouter()

@router.get("/", response_model=CustomResponses, name="Get categories")
async def get_categories(info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_categories(info=info, connPostgreSQL=connPostgreSQL)
