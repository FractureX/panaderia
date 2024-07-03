from fastapi import status
from fastapi.responses import JSONResponse
from typing import Any
import pyodbc

from src.category.domain.models import (
    Category
)
from src.shared.models.response import (
    messages
)
from src.shared.utils import (
    queries
)
from src.shared.infrastructure.database.sqlserver import SQLServer
from src.shared.models.response import messages
from src.shared.models.response.response import getJsonResponse
from src.shared.utils import auths_per_user
from src.shared.utils.functions.functions import (
    validate_crud_action, 
    to_json
)
from src.shared.models.response import messages

def get_categories(info: dict[str, Any], connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=int(info.get("id")), module=auths_per_user.Module.CATEGORY, crud=auths_per_user.Crud.SELECT, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        # Seleccionar categorías
        result = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_CATEGORY_SELECT_ALL)
        validation = validate_crud_action(result=result, message=messages.getDataNotFound("Categorías"), connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = [to_json(object=Category(**data)) for data in result]
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=result)
    except Exception as e:
        print(f"Exception: {e}")
        connSQLServer.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})
