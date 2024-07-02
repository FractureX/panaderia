from enum import Enum
from fastapi import status
from fastapi.responses import JSONResponse
from pyodbc import Connection
from pydantic import PositiveInt

from src.shared.models.response import messages
from src.shared.models.response.response import getJsonResponse
from src.user.domain.models import User
from src.shared.infrastructure.database.sqlserver import SQLServer
from src.shared.utils import queries
from src.shared.utils import ids

class Crud(Enum):
    SELECT = "Select"
    CREATE = "Create"
    UPDATE = "Update"
    DELETE = "Delete"

class Role(Enum):
    ADMINISTRADOR   = ids.SQLSERVER_ROLE_ADMINISTRATOR
    PERSONAL        = ids.SQLSERVER_ROLE_CASHIER

class Module(Enum):
    CATEGORY    = "CATEGORY"
    PRODUCT     = "PRODUCT"
    USER        = "USER"
    
module_permissions = {
    Module.CATEGORY: {
        Role.ADMINISTRADOR: [Crud.SELECT, Crud.CREATE, Crud.UPDATE, Crud.DELETE],
        Role.PERSONAL: [Crud.SELECT]
    },
    Module.PRODUCT: {
        Role.ADMINISTRADOR: [Crud.SELECT, Crud.CREATE, Crud.UPDATE, Crud.DELETE],
        Role.PERSONAL: [Crud.SELECT, Crud.UPDATE]
    },
    Module.USER: {
        Role.ADMINISTRADOR: [Crud.SELECT, Crud.CREATE, Crud.UPDATE, Crud.DELETE],
        Role.PERSONAL: [Crud.SELECT, Crud.UPDATE]
    }
}

def _get_module_permissions(crud: Crud, role: Role, module: Module) -> bool:
    return crud in module_permissions.get(module, {}).get(role, [])

def validate_user_module(id_user: PositiveInt, module: Module, crud: Crud, connSQLServer: Connection) -> bool | JSONResponse:
    result = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_USER_SELECT_BY_ID, vars=(id_user,))
    if isinstance(result, JSONResponse): return result
    user_db = User(**result[0])
    if not _get_module_permissions(crud=crud, role=Role(user_db.id_role), module=module):
        return getJsonResponse(status_code=status.HTTP_401_UNAUTHORIZED, success=False, message=messages.USER_NO_PERMISSION, data={})
    return True