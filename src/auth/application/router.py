from fastapi import (
    APIRouter, 
    Depends
)
from fastapi.security import OAuth2PasswordRequestForm
from pyodbc import Connection

from src.auth.infrastructure import service
from src.shared.infrastructure.database.sqlserver import SQLServer

router = APIRouter()

@router.post("/", name="Iniciar sesión para obtener el access token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), connSQLServer: Connection = Depends(SQLServer.get_connection)):
    result = await service.login(form_data=form_data, connSQLServer=connSQLServer)
    return result
