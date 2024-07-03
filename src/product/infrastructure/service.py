from fastapi import (
    status, 
    UploadFile
)
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from typing import Any
import pyodbc

from src.shared.utils.tables import SQLServerTables
from src.product.domain.models import (
    Product,
    CreateProduct,
    UpdateProduct
)
from src.shared.utils.functions import functions
from src.shared.models.response import (
    messages
)
from src.shared.utils import (
    queries,
)
from src.shared.infrastructure.database.sqlserver import SQLServer
from src.shared.models.response import messages
from src.shared.models.response.response import getJsonResponse
from src.shared.utils import auths_per_user

async def post_product(*, info: dict[str, Any], product: CreateProduct, image: UploadFile | None = None, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.CREATE, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(table=SQLServerTables.PRODUCT.value, vars=functions.to_json(object=product), create=True, connSQLServer=connSQLServer)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Dump insert model
        insert = functions.to_json(object=product)
        print(f"insert: {str(insert)}")
        inventory = {"quantity": insert.get("quantity")}
        
        # Insertar producto
        del(insert["quantity"])
        result = SQLServer.insert(conn=connSQLServer, query=queries.POSTGRESQL_PRODUCT_INSERT, vars=(insert.get("name"), insert.get("description"), insert.get("price"), insert.get("id_category"), insert.get("id_status")))
        validation = functions.validate_crud_action(result=result, message=messages.INSERT_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Obtener id insertado
        id = result[0].get("id")
        
        # Save image
        await functions.save_image(module=auths_per_user.Module.PRODUCT, id=id, image=image, data=insert, save_in_directory=True)
        
        # Actualizar la imagen
        result = SQLServer.update(conn=connSQLServer, query=queries.POSTGRESQL_PRODUCT_UPDATE_IMAGE, vars=(insert.get("image"), id))
        validation = functions.validate_crud_action(result=result, message=messages.INSERT_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Insertar inventario
        inventory.update({"id_product": id})
        inventory.update({"id_status": insert.get("id_status")})
        print(f"inventory: {str(inventory)}")
        result = SQLServer.update(conn=connSQLServer, query=queries.POSTGRESQL_INVENTORY_INSERT, vars=(inventory.get("id_product"), inventory.get("quantity"), inventory.get("id_status")))
        validation = functions.validate_crud_action(result=result, message=messages.INSERT_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Commit
        connSQLServer.commit()
        
        return getJsonResponse(status_code=status.HTTP_201_CREATED, success=True, message="", data=insert)
    except Exception as e:
        print(f"Exception: {e}")
        connSQLServer.rollback()
        if (insert):
            if insert.get("image", None) is not None:
                functions.delete_image(image_url=insert.get("image"))
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=messages.EXCEPTION, data={})

def get_products(info: dict[str, Any], connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.SELECT, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        result = SQLServer.select(connSQLServer, query=queries.POSTGRESQL_PRODUCT_SELECT_ALL)
        validation = functions.validate_crud_action(result=result, message=messages.getDataNotFound("Products"), connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = [functions.to_json(object=Product(**row)) for row in result]
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=result)
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def get_product_by_id(info: dict[str, Any], id: PositiveInt, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.SELECT, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result = functions.validate_ids(connSQLServer=connSQLServer, table=SQLServerTables.PRODUCT.value, vars={"id": id})
        validation = functions.validate_crud_action(result=result, message=messages.getDataNotFound("Product"), connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_PRODUCT_SELECT_BY_ID, vars=(id,))
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=functions.to_json(object=Product(**result[0])))
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def get_product_by_id_category(info: dict[str, Any], id_category: PositiveInt, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.SELECT, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result = functions.validate_ids(connSQLServer=connSQLServer, table=SQLServerTables.CATEGORY.value, vars={"id": id_category})
        validation = functions.validate_crud_action(result=result, message=messages.getDataNotFound("Categoría"), connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_PRODUCT_SELECT_BY_ID_CATEGORY, vars=(id_category,), print_data=True)
        validation = functions.validate_crud_action(result=result, message=messages.getDataNotFound("Productos"), connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = [functions.to_json(object=Product(**data)) for data in result]
        
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=result)
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

async def put_product(*, info: dict[str, Any], product: UpdateProduct, image: UploadFile | None = None, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.UPDATE, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result = functions.validate_ids(table=SQLServerTables.PRODUCT.value, vars=functions.to_json(object=product), connSQLServer=connSQLServer)
        validation = functions.validate_crud_action(result=result, message=result, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Obtener imagen actual
        current_image: str = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_PRODUCT_SELECT_BY_ID, vars=(product.id,))[0].get("image")
        
        # Product model dump
        update = functions.to_json(object=product)
        
        # Update image path
        await functions.save_image(module=auths_per_user.Module.PRODUCT, id=product.id, image=current_image if image is None else image, data=update)
        
        # Update product
        result = SQLServer.update(conn=connSQLServer, query=queries.POSTGRESQL_PRODUCT_UPDATE, vars=(update.get("name"), update.get("description"), update.get("price"), update.get("image"), update.get("id_category"), update.get("id_status"), update.get("id")), print_data=True)
        validation = functions.validate_crud_action(connSQLServer=connSQLServer, result=result, message=messages.UPDATE_INTERNAL_SERVER_ERROR)
        if (isinstance(validation, JSONResponse)):
            if update.get("image", None) is not None:
                functions.delete_image(image_url=update.get("image"))
            return validation
        
        # Commit
        connSQLServer.commit()
        
        # Delete actual image
        if image is not None and current_image is not None:
            functions.delete_image(image_url=current_image)
        
        # Save image
        if image is not None:
            await functions.save_image(module=auths_per_user.Module.PRODUCT, id=product.id, image=image, data=update, save_in_directory=True)
        
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=update)
    except Exception as e:
        print(f"Exception: {e}")
        connSQLServer.rollback()
        # Delete temp image
        if (update.get("image", None) is not None and "temp-" in update.get("image")):
            functions.delete_image(image_url=update.get("image"))
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def delete_product(info: dict[str, Any], id: PositiveInt, connSQLServer: pyodbc.Connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.DELETE, connSQLServer=connSQLServer)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(table=SQLServerTables.PRODUCT.value, vars={"id": id}, connSQLServer=connSQLServer)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Obtener imagen
        image = SQLServer.select(conn=connSQLServer, query=queries.POSTGRESQL_PRODUCT_SELECT_BY_ID, vars=(id,))[0].get("image")
        
        # Delete product
        result = SQLServer.update(conn=connSQLServer, query=queries.POSTGRESQL_PRODUCT_DELETE, vars=(id,), print_data=True)
        validation = functions.validate_crud_action(result=result, message=messages.DELETE_INTERNAL_SERVER_ERROR, connSQLServer=connSQLServer)
        if (isinstance(validation, JSONResponse)): return validation
        
        if image is not None:
            functions.delete_image(image_url=image)
        
        # Commit
        connSQLServer.commit()
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data={"id": id})
    except Exception as e:
        print(f"Exception: {e}")
        connSQLServer.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})
