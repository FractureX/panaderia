import os
from jose import jwt
from decimal import Decimal
from bson import ObjectId
from fastapi import status, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pyodbc import Connection
from typing import Any
from pydantic import (
    PositiveInt, 
    StrictStr
)
from datetime import (
    datetime, 
    timedelta,
    timezone
)
from passlib.context import CryptContext

from src.shared.config.Environment import get_environment_variables
from src.shared.utils import ids
from src.shared.utils.tables import (
    PostgreSQLTables,
)
from src.shared.infrastructure.database.sqlserver import SQLServer
from src.shared.models.response import messages
from src.shared.models.response.response import getJsonResponse
from src.shared.utils.auths_per_user import Module
from src.shared.utils import queries

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
_env = get_environment_variables()

def to_tuple(vars: dict[str, Any], exclude: list[str] = None, include_id: bool = False, invert_id: bool = False) -> tuple:
    if (exclude):
        for column in exclude:
            del(vars[column])
    if (vars.get('id', None) is not None):
        id: int = vars["id"]
        del(vars["id"])
        returnValue: tuple | list
        if include_id:
            returnValue = [value for value in vars.values()]
            returnValue.insert(len(returnValue) if invert_id else 0, id)
            returnValue = tuple(returnValue)
        else:
            returnValue = tuple([value for value in vars.values()])
    else:
        returnValue = tuple([value for value in vars.values()])
    return returnValue

def validate_ids(*, table: str, vars: dict[str, int], create: bool = False, connSQLServer: SQLServer = None) -> str | JSONResponse:
    print('------------------ validate_ids ------------------')
    returnStrValue: str = ""
    for enum_table in PostgreSQLTables:
        if (table == enum_table.value):
            if vars.get('id', None) is not None:
                vars[f'id_{enum_table.value}'] = vars['id']
    if (vars.get('id', None) is not None): del(vars['id'])
    try:
        for enum_table in PostgreSQLTables:
            if (vars.get(f"id_{enum_table.value}", None) is not None):
                if (enum_table.value != table or (enum_table.value == table and not create)):
                    result = SQLServer.select(conn=connSQLServer, query=queries.getSelectQueryById(enum_table.value), vars=(vars[f'id_{enum_table.value}'],))
                    if (type(result) != list): raise result
                    if (len(returnStrValue) == 0): returnStrValue += messages.getDataNotFound(dataName=f"{enum_table.value.replace('_', ' ').capitalize()} {vars[f'id_{enum_table.value}']}") if len(result) == 0 else ""
                    else: returnStrValue += ", " + messages.getDataNotFound(dataName=f"{enum_table.value.replace('_', ' ').capitalize()} {vars[f'id_{enum_table.value}']}") if len(result) == 0 else ""
    except Exception as e:
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})
    return returnStrValue

async def validate_user(*, id: PositiveInt | None = None, form_data: OAuth2PasswordRequestForm | None = None, connSQLServer: Connection) -> dict | JSONResponse:
    try:
        if id is not None:
            user = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_USER_SELECT_BY_ID, vars=(id,), print_data=True)
        if form_data is not None:
            user = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_USER_SELECT_BY_EMAIL, vars=(form_data.username,), print_data=True)
        validation = validate_crud_action(connSQLServer=connSQLServer, result=user, message=messages.getDataNotFound("Usuario"))
        if (isinstance(validation, JSONResponse)): return validation
        user = user[0]
        
        # Validar que el usuario esté activo
        if (user.get("id_status") != ids.SQLSERVER_STATUS_ACTIVE): return getJsonResponse(status_code=status.HTTP_401_UNAUTHORIZED, success=False, message=messages.USER_NO_ACTIVE, data={})

        # Validar que la contraseña sea la misma
        if form_data is not None:
            if (not verify_password(password=form_data.password, hashed_password=user.get("password"))): 
                return getJsonResponse(headers={"WWW-Authenticate": "Bearer"}, status_code=status.HTTP_401_UNAUTHORIZED, success=False, message=messages.CREDENTIALS_INVALID, data={})
        
        # Retornar cuando sea para iniciar sesión
        if form_data is not None:
            return {
                "access_token": create_token(user.get("id"))
            }
        
        # Retornar cuando no sea para iniciar sesión
        return {
            "id": user.get("id")
        }
    except Exception as e:
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def create_token(id: PositiveInt, expire_delta: timedelta = timedelta(days=30)) -> StrictStr:
    expire_time = datetime.now(timezone.utc) + expire_delta
    payload = {
        "sub": str(id),
        "exp": expire_time
    }
    return jwt.encode(claims=payload, key=_env.JWT_SECRET_KEY, algorithm=_env.JWT_ALGORITHM)

def verify_password(password: StrictStr, hashed_password: StrictStr) -> bool:
    return bcrypt_context.verify(secret=password, hash=hashed_password)

async def save_image(module: Module, id: int, image: UploadFile | str, data: dict, save_in_directory: bool = False):
    if image is None or isinstance(image, str):
        data.update({"image": None if image is None else image})
        return
    filename = image.filename.split('.')
    extension = filename[len(filename) - 1].lower()
    filename = f"{id}.{extension}"
    
    file_location = os.path.join(module.value, filename)
    
    file_url = f"https://vainilla-backend-52fz.onrender.com/static/{module.value}/{filename}"
    data.update({"image": file_url})
    
    # Guardar imagen
    if save_in_directory:
        with open(file_location, "wb") as f:
            f.write(await image.read())
        
def delete_image(image_url: str, temp_image: bool = False):
    try:
        base = image_url.split("/static/")[1].split("/")
        module = base[0]
        filename = base[1]
        file_location = os.path.join(module, filename if not temp_image else 'temp-' + filename)
        os.remove(f"{file_location}")
    except Exception as e:
        print(f"e: {str(e)}")

def validate_crud_action(*, result, message: str, check_len: bool = True, connSQLServer: Connection = None) -> JSONResponse | None:
    if (isinstance(result, JSONResponse) or (isinstance(result, bool) and not result)):
        if (isinstance(result, JSONResponse)):
            return result
        if (connSQLServer is not None): connSQLServer.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=message, data={})
    if check_len:
        if (isinstance(result, list) and len(result) == 0) or (isinstance(result, str) and len(result) > 0):
            return getJsonResponse(status_code=status.HTTP_404_NOT_FOUND, success=False, message=message, data=[{}])

def to_json(object) -> dict[str, Any]:
    if hasattr(object, 'model_dump'):
        json: dict = object.model_dump()
    else:
        json = object
    for key in json.keys():
        if (isinstance(json[key], ObjectId)):
            json[key] = str(json[key])
        if (isinstance(json[key], datetime)):
            json[key] = json[key].isoformat()
        if (isinstance(json[key], Decimal)):
            json[key] = float(json[key])
    return json
