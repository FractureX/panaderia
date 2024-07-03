from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from typing import Any
import pyodbc

from src.shared.utils.functions import functions
from src.shared.models.response import (
    messages
)
from src.inventory.domain.models import (
    UpdateInventoryQuantity
)
from src.shared.utils import (
    queries
)
from src.shared.infrastructure.database.sqlserver import SQLServer
from src.shared.models.response import messages
from src.shared.models.response.response import getJsonResponse
from src.shared.utils import auths_per_user
from src.shared.utils.tables import SQLServerTables

def put_quantity_add(info: dict[str, Any], inventory: UpdateInventoryQuantity, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.USER, crud=auths_per_user.Crud.UPDATE, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result = functions.validate_ids(table=SQLServerTables.PRODUCT.value, vars=functions.to_json(object=inventory), connSQLServer=connSQLServer)
        validation = functions.validate_crud_action(result=result, message=result, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Update inventory
        result = SQLServer.update(conn=connSQLServer, query=queries.POSTGRESQL_INVENTORY_UPDATE_ADD, vars=(inventory.quantity, inventory.id_product), print_data=True)
        validation = functions.validate_crud_action(result=result, message=messages.UPDATE_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Commit
        connSQLServer.commit()
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=functions.to_json(object=inventory))
    except Exception as e:
        print(f"Exception: {e}")
        connSQLServer.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})
