from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from psycopg2.extensions import connection
from typing import Any

from src.shared.utils.functions import functions
from src.shared.models.response import (
    messages
)
from src.user.domain.models import (
    User,
    CreateUser,
    UpdateUser, 
    UpdateCredential
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
from src.shared.utils.tables import PostgreSQLTables

def post_user(info: dict[str, Any], user: CreateUser, connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.CREATE, connPostgreSQL=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(table=PostgreSQLTables.USER.value, vars=functions.to_json(object=user), create=True, connSQLServer=connPostgreSQL)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Insert user
        userInsertData = user.model_copy()
        del(userInsertData.credential)
        userResult = SQLServer.insert(conn=connPostgreSQL, query=queries.POSTGRESQL_USER_INSERT, vars=functions.to_tuple(vars=functions.to_json(object=userInsertData)))
        validation = functions.validate_crud_action(result=userResult, message=messages.INSERT_INTERNAL_SERVER_ERROR, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Insert credential
        credentialResult = SQLServer.insert(conn=connPostgreSQL, query=queries.POSTGRESQL_CREDENTIAL_INSERT, vars=(user.email, get_password_hash(user.credential.password)))
        validation = functions.validate_crud_action(result=credentialResult, message=messages.INSERT_INTERNAL_SERVER_ERROR, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Obtener id del usuario
        #id_user = PostgreSQL.select(conn=connPostgreSQL, query=queries.POSTGRESQL_USER_SELECT_BY_EMAIL, vars=(user.email,))[0]["id"]
        print(f"userResult: {str(userResult)}")
        id_user = userResult[0].get("id")
        returnValue = functions.to_json(object=user)
        returnValue.update({"id": id_user})
        del(returnValue["credential"])
        
        # Commit
        connPostgreSQL.commit()
        return getJsonResponse(status_code=status.HTTP_201_CREATED, success=True, message="", data=returnValue)
    except Exception as e:
        print(f"Exception: {e}")
        connPostgreSQL.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=messages.EXCEPTION, data={})

def get_user(info: dict[str, Any], connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.SELECT, connPostgreSQL=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        result = SQLServer.select(conn=connPostgreSQL, query=queries.POSTGRESQL_USER_SELECT_ALL)
        validation = functions.validate_crud_action(result=result, message=messages.getDataNotFound("Users"), connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = [functions.to_json(object=User(**row)) for row in result]
        for user in result:
            del(user["credential"])
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=result)
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def get_user_by_id(info: dict[str, Any], id: PositiveInt, connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.SELECT, connPostgreSQL=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(table=PostgreSQLTables.USER.value, vars={"id": id}, connSQLServer=connPostgreSQL)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = SQLServer.select(conn=connPostgreSQL, query=queries.POSTGRESQL_USER_SELECT_BY_ID, vars=(id,))
        user: User = User(**result[0])
        del(user.credential)
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=functions.to_json(object=user))
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def get_user_client_by_id_institution(info: dict[str, Any], id_institution: PositiveInt, connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.SELECT, connPostgreSQL=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(connSQLServer=connPostgreSQL, table=PostgreSQLTables.INSTITUTION.value, vars={"id": id_institution})
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = SQLServer.select(connPostgreSQL, query=queries.POSTGRESQL_USER_CLIENT_SELECT_BY_ID_INSTITUTION, vars=(id_institution,))
        validation = functions.validate_crud_action(result=result, message=messages.getDataNotFound("Users"), connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = [functions.to_json(object=User(**row)) for row in result]
        for data in result:
            del(data["credential"])
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=result)
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def get_user_client_by_id_institution_criteria(info: dict[str, Any], id_institution: PositiveInt, criteria: str, connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.SELECT, connPostgreSQL=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(table=PostgreSQLTables.INSTITUTION.value, vars={"id_institution": id_institution}, connSQLServer=connPostgreSQL)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = SQLServer.select(connPostgreSQL, query=queries.POSTGRESQL_USER_CLIENT_SELECT_BY_ID_INSTITUTION_CRITERIA, vars=(id_institution, f"%{criteria}%", f"%{criteria}%", f"%{criteria}%"))
        validation = functions.validate_crud_action(result=result, message=messages.getDataNotFound("Users"), connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = [functions.to_json(object=User(**row)) for row in result]
        for data in result:
            del(data["credential"])
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=result)
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def put_user(info: dict[str, Any], user: UpdateUser, connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.UPDATE, connPostgreSQL=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result = functions.validate_ids(table=PostgreSQLTables.USER.value, vars=functions.to_json(object=user), connSQLServer=connPostgreSQL)
        validation = functions.validate_crud_action(result=result, message=result, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        if (hasattr(user, 'credential')):
            if (user.credential is not None):
                # Update credential
                update_credential: UpdateCredential = user.credential.model_copy()
                update_credential.password = get_password_hash(update_credential.password)
                result = SQLServer.update(conn=connPostgreSQL, query=queries.POSTGRESQL_CREDENTIAL_UPDATE, vars=(user.email, update_credential.password, user.id))
                validation = functions.validate_crud_action(result=result, message=messages.UPDATE_INTERNAL_SERVER_ERROR, connSQLServer=connPostgreSQL)
                if (isinstance(validation, JSONResponse)): return validation
        
        # Update user
        update_user: UpdateUser = user.model_copy()
        if (hasattr(update_user, 'credential')): del(update_user.credential)
        del(update_user.id_role)
        result = SQLServer.update(conn=connPostgreSQL, query=queries.POSTGRESQL_USER_UPDATE, vars=functions.to_tuple(vars=functions.to_json(object=update_user), include_id=True, invert_id=True))
        validation = functions.validate_crud_action(result=result, message=messages.UPDATE_INTERNAL_SERVER_ERROR, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Commit
        connPostgreSQL.commit()
        if (hasattr(user, 'credential')): del(user.credential)
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=functions.to_json(object=user))
    except Exception as e:
        print(f"Exception: {e}")
        connPostgreSQL.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def inactivate_user(info: dict[str, Any], id: PositiveInt, connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.UPDATE, connPostgreSQL=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar que no sea el mismo usuario
        if (info == id): return getJsonResponse(status_code=status.HTTP_401_UNAUTHORIZED, success=False, message=messages.USER_UPDATE_INACTIVATE_SAME_USER, data={})
        
        # Validar IDs
        result_validate = functions.validate_ids(table=PostgreSQLTables.USER.value, vars={"id": id}, connSQLServer=connPostgreSQL)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Inhabilitar
        result = SQLServer.update(conn=connPostgreSQL, query=queries.POSTGRESQL_USER_UPDATE_INACTIVATE, vars=(id,))
        validation = functions.validate_crud_action(result=result, message=messages.UPDATE_INTERNAL_SERVER_ERROR, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Commit
        connPostgreSQL.commit()
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data={"id": id})
    except Exception as e:
        print(f"Exception: {e}")
        connPostgreSQL.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def activate_user(info: dict[str, Any], id: PositiveInt, connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.UPDATE, connPostgreSQL=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar que no sea el mismo usuario
        if (info == id): return getJsonResponse(status_code=status.HTTP_401_UNAUTHORIZED, success=False, message=messages.USER_UPDATE_ACTIVATE_SAME_USER, data={})
        
        # Validar IDs
        result_validate = functions.validate_ids(table=PostgreSQLTables.USER.value, vars={"id": id}, connSQLServer=connPostgreSQL)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Habilitar
        result = SQLServer.update(conn=connPostgreSQL, query=queries.POSTGRESQL_USER_UPDATE_ACTIVATE, vars=(id,))
        validation = functions.validate_crud_action(result=result, message=messages.UPDATE_INTERNAL_SERVER_ERROR, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Commit
        connPostgreSQL.commit()
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data={"id": id})
    except Exception as e:
        print(f"Exception: {e}")
        connPostgreSQL.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})
