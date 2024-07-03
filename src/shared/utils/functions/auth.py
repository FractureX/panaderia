from datetime import datetime, timedelta
from fastapi import (
    Depends, 
    status, 
    HTTPException
)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from psycopg2.extensions import connection
from pydantic import (
    EmailStr, 
    PositiveInt,
    StrictStr
)
from typing import Optional, Any

from src.shared.infrastructure.database.sqlserver import SQLServer
from src.shared.utils import queries
from src.user.domain.models import User
from src.shared.config.Environment import get_environment_variables

_env = get_environment_variables()

_bcrypt_context: CryptContext = CryptContext(schemes=["bcrypt"])
oauth2bearer = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(plain_password: str):
    return _bcrypt_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str):
    return _bcrypt_context.verify(secret=plain_password, hash=hashed_password)

def authenticate_user(conn: connection, email: EmailStr, plain_password: str) -> bool | User | JSONResponse:
    result = SQLServer.select(conn=conn, query=queries.POSTGRESQL_USER_SELECT_BY_USERNAME, vars=(email,))
    print(type(result))
    if (type(result) is not list): return result
    user: User = User(**result[0])
    if (len(result) == 0 or not verify_password(plain_password, user.credential.password)): return False
    return user

def create_access_token(id_user: PositiveInt, expires_delta: Optional[timedelta] = None):
    encode = {
        "sub": id_user, 
    }
    if (expires_delta):
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, _env.JWT_SECRET_KEY, algorithm=_env.JWT_ALGORITHM)

def get_current_user(token: StrictStr = Depends(oauth2bearer)):
    try:
        payload: dict[str, Any] = jwt.decode(token=token, key=_env.JWT_SECRET_KEY, algorithms=[_env.JWT_ALGORITHM])
        email: EmailStr = payload.get("sub")
        id_user: PositiveInt = payload.get("id")
        if (email is None or id_user is None): raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        return {"id_user": id_user, "email": email}
    except JWTError: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})