from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from typing import Any
import pyodbc

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
async def post_user(user: CreateUser, info: dict[str, Any] = Depends(validate_token), connSQLServer: pyodbc.Connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.post_user(info=info, user=user, connSQLServer=connSQLServer)

@router.get("/", response_model=CustomResponses, name="Get all users")
async def get_user(info: dict[str, Any] = Depends(validate_token), connSQLServer: pyodbc.Connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_users(info=info, connSQLServer=connSQLServer)

@router.get("/{id}", response_model=CustomResponse, name="Get user by id")
async def get_user_by_id(id: PositiveInt, info: dict[str, Any] = Depends(validate_token), connSQLServer: pyodbc.Connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_user_by_id(info=info, id=id, connSQLServer=connSQLServer)

@router.put("/modify", response_model=CustomResponse, name="Modify user")
async def put_user(user: UpdateUser, info: dict[str, Any] = Depends(validate_token), connSQLServer: pyodbc.Connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.put_user(info=info, user=user, connSQLServer=connSQLServer)

@router.delete("/delete/{id}", response_model=CustomResponse, name="Delete user")
async def activate_user(id: PositiveInt, info: dict[str, Any] = Depends(validate_token), connSQLServer: pyodbc.Connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.delete_user(info=info, id=id, connSQLServer=connSQLServer)
