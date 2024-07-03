from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from typing import Any
import pyodbc

from src.shared.utils.functions import functions
from src.shared.models.response import (
    messages
)
from src.user.domain.models import (
    User,
    CreateUser,
    UpdateUser
)
from src.shared.utils import (
    queries
)
from src.shared.infrastructure.database.sqlserver import SQLServer
from src.shared.models.response import messages
from src.shared.models.response.response import getJsonResponse
from src.shared.utils.functions.auth import (
    get_password_hash
)
from src.shared.utils import auths_per_user
from src.shared.utils.tables import SQLServerTables

def post_user(info: dict[str, Any], user: CreateUser, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.CREATE, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(table=SQLServerTables.USER.value, vars=functions.to_json(object=user), create=True, connSQLServer=connSQLServer)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Insert user
        user.password = get_password_hash(plain_password=user.password)
        result = SQLServer.insert(conn=connSQLServer, query=queries.POSTGRESQL_USER_INSERT, vars=functions.to_tuple(vars=functions.to_json(object=user)))
        validation = functions.validate_crud_action(result=result, message=messages.INSERT_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Commit
        connSQLServer.commit()
        user = functions.to_json(object=user)
        user.update({"id": result[0].get("id")})
        del(user["password"])
        return getJsonResponse(status_code=status.HTTP_201_CREATED, success=True, message="", data=user)
    except Exception as e:
        print(f"Exception: {e}")
        connSQLServer.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=messages.EXCEPTION, data={})

def get_users(info: dict[str, Any], connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.SELECT, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        result = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_USER_SELECT_ALL)
        validation = functions.validate_crud_action(result=result, message=messages.getDataNotFound("Users"), connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = [functions.to_json(object=User(**row)) for row in result]
        for user in result:
            del(user["password"])
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=result)
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def get_user_by_id(info: dict[str, Any], id: PositiveInt, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.SELECT, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(table=SQLServerTables.USER.value, vars={"id": id}, connSQLServer=connSQLServer)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_USER_SELECT_BY_ID, vars=(id,))
        user: User = User(**result[0])
        del(user.password)
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=functions.to_json(object=user))
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def put_user(info: dict[str, Any], user: UpdateUser, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.UPDATE, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result = functions.validate_ids(table=SQLServerTables.USER.value, vars=functions.to_json(object=user), connSQLServer=connSQLServer)
        validation = functions.validate_crud_action(result=result, message=result, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Update user
        user.password = get_password_hash(plain_password=user.password)
        result = SQLServer.update(conn=connSQLServer, query=queries.POSTGRESQL_USER_UPDATE, vars=functions.to_tuple(vars=functions.to_json(object=user), include_id=True, invert_id=True), print_data=True)
        validation = functions.validate_crud_action(result=result, message=messages.UPDATE_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Commit
        connSQLServer.commit()
        if (hasattr(user, 'password')): del(user.password)
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=functions.to_json(object=user))
    except Exception as e:
        print(f"Exception: {e}")
        connSQLServer.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def delete_user(info: dict[str, Any], id: PositiveInt, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.UPDATE, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result = functions.validate_ids(table=SQLServerTables.USER.value, vars={"id": id}, connSQLServer=connSQLServer)
        validation = functions.validate_crud_action(result=result, message=result, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Validar que no sea el mismo usuario
        if id == info.get("id"): return getJsonResponse(status_code=status.HTTP_401_UNAUTHORIZED, success=False, message=messages.USER_DELETE_SAME_USER, data={})
        
        # Delete user
        result = SQLServer.update(conn=connSQLServer, query=queries.POSTGRESQL_USER_DELETE, vars=(id,), print_data=True)
        validation = functions.validate_crud_action(result=result, message=messages.DELETE_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Commit
        connSQLServer.commit()
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data={"id": id})
    except Exception as e:
        print(f"Exception: {e}")
        connSQLServer.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})
