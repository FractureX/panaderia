from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from psycopg2.extensions import connection
from pydantic import StrictStr
from typing import Any

from src.user.domain.models import (
    CreateUser,
    UpdateUser
)
from src.user.infrastructure import service
from src.shared.models.response.response import (
    CustomResponse,
    CustomResponses
)
from src.shared.infrastructure.database.sqlserver import SQLServer
from src.auth.utils.functions.functions import validate_token

router = APIRouter()

@router.post("/add", response_model=CustomResponse, name="Add user")
async def post_user(user: CreateUser, info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.post_user(info=info, user=user, connPostgreSQL=connPostgreSQL)

@router.get("/", response_model=CustomResponses, name="Get all users")
async def get_user(info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_user(info=info, connPostgreSQL=connPostgreSQL)

@router.get("/{id}", response_model=CustomResponse, name="Get user by id")
async def get_user_by_id(id: PositiveInt, info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_user_by_id(info=info, id=id, connPostgreSQL=connPostgreSQL)

@router.get("/client/{id_institution}", response_model=CustomResponses, name="Get clients user by institution id")
async def get_user_client_by_id_institution(id_institution: PositiveInt, info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    print("Hola 1")
    if (type(info) == JSONResponse): return info
    return service.get_user_client_by_id_institution(info=info, id_institution=id_institution, connPostgreSQL=connPostgreSQL)

@router.get("/client/{id_institution}/{criteria}", response_model=CustomResponses, name="Get clients user by institution id and criteria")
async def get_user_client_by_id_institution_criteria(id_institution: PositiveInt, criteria: StrictStr, info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if criteria == ':criteria': criteria = ""
    if (type(info) == JSONResponse): return info
    return service.get_user_client_by_id_institution_criteria(info=info, id_institution=id_institution, criteria=criteria, connPostgreSQL=connPostgreSQL)

@router.put("/modify", response_model=CustomResponse, name="Modify user")
async def put_user(user: UpdateUser, info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.put_user(info=info, user=user, connPostgreSQL=connPostgreSQL)

@router.delete("/inactivate/{id_institution}/{id}", response_model=CustomResponse, name="Inactivate user")
async def inactivate_user(id: PositiveInt, info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.inactivate_user(info=info, id=id, connPostgreSQL=connPostgreSQL)

@router.put("/activate/{id_institution}/{id}", response_model=CustomResponse, name="Activate user")
async def activate_user(id: PositiveInt, info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.activate_user(info=info, id=id, connPostgreSQL=connPostgreSQL)
