from fastapi import (
    Depends,
    status
)
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from pydantic import (
    StrictStr,
    PositiveInt
)
from jose import (
    jwt, 
    JWTError
)
from jose.exceptions import ExpiredSignatureError
from typing import Any
from psycopg2.extensions import connection
import asyncpg

from src.shared.utils.functions.functions import bcrypt_context, validate_user
from src.shared.models.response import messages
from src.shared.infrastructure.database.sqlserver import SQLServer
from src.shared.config.Environment import get_environment_variables
from src.shared.models.response.response import getJsonResponse

_env = get_environment_variables()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")

def hash_password(password: StrictStr) -> StrictStr:
    return bcrypt_context.hash(password)

async def validate_token(connPostgreSQL: connection | asyncpg.Connection = Depends(SQLServer.get_connection), token: StrictStr = Depends(oauth2_scheme)) -> dict[str, Any] | JSONResponse:
    print("------------------- validate_token -------------------")
    id: PositiveInt
    try:
        token_decode = jwt.decode(token=token, key=_env.JWT_SECRET_KEY, algorithms=[_env.JWT_ALGORITHM])
        id = int(token_decode.get("sub"))
        if (id is None): 
            return getJsonResponse(headers={"WWW-Authenticate": "Bearer"}, status_code=status.HTTP_401_UNAUTHORIZED, success=False, message=messages.CREDENTIALS_COULD_NOT_VALIDATE, data={})
    except ExpiredSignatureError as e:
        print(str(e))
        return getJsonResponse(headers={"WWW-Authenticate": "Bearer"}, status_code=status.HTTP_401_UNAUTHORIZED, success=False, message=messages.CREDENTIALS_EXPIRED_SIGNATURE, data={})
    except JWTError as e:
        print(str(e))
        return getJsonResponse(headers={"WWW-Authenticate": "Bearer"}, status_code=status.HTTP_401_UNAUTHORIZED, success=False, message=messages.CREDENTIALS_COULD_NOT_VALIDATE, data={})
    
    # Validar usuario
    data = await validate_user(connSQLServer=connPostgreSQL, id=id)
    return data