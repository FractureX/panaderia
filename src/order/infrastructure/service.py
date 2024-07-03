from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from typing import Any
import pyodbc

from src.shared.utils.functions import functions
from src.shared.models.response import (
    messages
)
from src.order.domain.models import (
    Order,
    CreateOrder,
    CreateOrderProduct,
    CreateInvoice
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

def post_order(info: dict[str, Any], order: CreateOrder, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.ORDER, crud=auths_per_user.Crud.CREATE, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate

        # Validar IDs
        result_validate = functions.validate_ids(table=SQLServerTables.ORDER.value, vars=functions.to_json(object=order), create=True, connSQLServer=connSQLServer)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation

        # Insert order
        result = SQLServer.insert(conn=connSQLServer, query=queries.POSTGRESQL_ORDER_INSERT, vars=(order.id_user,))
        validation = functions.validate_crud_action(result=result, message=messages.INSERT_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation

        # Commit
        connSQLServer.commit()
        order = functions.to_json(object=order)
        order.update({"id": result[0].get("id")})
        return getJsonResponse(status_code=status.HTTP_201_CREATED, success=True, message="", data=order)
    except Exception as e:
        print(f"Exception: {e}")
        connSQLServer.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=messages.EXCEPTION, data={})

def get_orders(info: dict[str, Any], connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.ORDER, crud=auths_per_user.Crud.SELECT, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        result = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_ORDER_SELECT_ALL)
        validation = functions.validate_crud_action(result=result, message=messages.getDataNotFound("Ordenes"), connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = [functions.to_json(object=Order(**row)) for row in result]
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=result)
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def get_order_by_id(info: dict[str, Any], id: PositiveInt, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.ORDER, crud=auths_per_user.Crud.SELECT, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(table=SQLServerTables.ORDER.value, vars={"id": id}, connSQLServer=connSQLServer)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_ORDER_SELECT_BY_ID, vars=(id,))
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=functions.to_json(object=result[0]))
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def post_order_product(info: dict[str, Any], order: CreateOrderProduct, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.ORDER, crud=auths_per_user.Crud.CREATE, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate

        # Validar IDs
        result_validate = functions.validate_ids(table=SQLServerTables.ORDER.value, vars=functions.to_json(object=order), create=True, connSQLServer=connSQLServer)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation

        # Stock del producto
        product = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_INVENTORY_SELECT_BY_ID_PRODUCT, vars=(order.id_product,))[0]
        
        if product.get("quantity") < order.quantity:
            return getJsonResponse(status_code=status.HTTP_400_BAD_REQUEST, success=False, message="La cantidad es mayor", data={})
        
        # Insert product order
        result = SQLServer.insert(conn=connSQLServer, query=queries.POSTGRESQL_ORDER_ITEM_INSERT, vars=(order.id_order, order.id_product, order.quantity, product.get("price")))
        validation = functions.validate_crud_action(result=result, message=messages.INSERT_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation

        # Actualizar el total
        total = SQLServer.update(conn=connSQLServer, query=queries.POSTGRESQL_ORDER_UPDATE_TOTAL, vars=(order.id_order, order.id_order))
        validation = functions.validate_crud_action(result=total, message=messages.INSERT_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Commit
        connSQLServer.commit()
        order = functions.to_json(object=order)
        order.update({"id": result[0].get("id")})
        return getJsonResponse(status_code=status.HTTP_201_CREATED, success=True, message="", data=order)
    except Exception as e:
        print(f"Exception: {e}")
        connSQLServer.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=messages.EXCEPTION, data={})

def post_invoice(info: dict[str, Any], order: CreateInvoice, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.ORDER, crud=auths_per_user.Crud.CREATE, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate

        # Validar IDs
        result_validate = functions.validate_ids(table=SQLServerTables.ORDER.value, vars=functions.to_json(object=order), create=True, connSQLServer=connSQLServer)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation

        # Insert invoice
        result = SQLServer.insert(conn=connSQLServer, query=queries.POSTGRESQL_INVOICE_INSERT, vars=(order.id_order, order.id_order))
        validation = functions.validate_crud_action(result=result, message=messages.INSERT_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation

        # Update order item to 'Pagado'
        update = SQLServer.update(conn=connSQLServer, query=queries.POSTGRESQL_ORDER_ITEM_UPDATE_PAGADO, vars=(order.id_order,))
        validation = functions.validate_crud_action(result=update, message=messages.UPDATE_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation

        # Update order to 'Pagado'
        update = SQLServer.update(conn=connSQLServer, query=queries.POSTGRESQL_ORDER_UPDATE_PAGADO, vars=(order.id_order,))
        validation = functions.validate_crud_action(result=update, message=messages.UPDATE_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Update product stock
        products = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_ORDER_ITEM_SELECT_BY_ID_ORDER, vars=(order.id_order,))
        
        for product in products:
            update = SQLServer.update(conn=connSQLServer, query=queries.POSTGRESQL_INVENTORY_UPDATE_STOCK, vars=(order.id_order, product.get("id_product"), product.get("id_product")))
            validation = functions.validate_crud_action(result=update, message=messages.UPDATE_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
            if (isinstance(validation, JSONResponse)): return validation
        
        # Commit
        connSQLServer.commit()
        order = functions.to_json(object=order)
        order.update({"id": result[0].get("id")})
        return getJsonResponse(status_code=status.HTTP_201_CREATED, success=True, message="", data=order)
    except Exception as e:
        print(f"Exception: {e}")
        connSQLServer.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=messages.EXCEPTION, data={})
