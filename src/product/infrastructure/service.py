from fastapi import (
    status, 
    UploadFile
)
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from pymongo import MongoClient
from psycopg2.extensions import connection
from typing import Any

from src.shared.utils.tables import PostgreSQLTables
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

async def post_product(*, info: dict[str, Any], product: CreateProduct, image: UploadFile | None = None, connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.CREATE, connSQLServer=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(table=PostgreSQLTables.PRODUCT.value, vars=functions.to_json(object=product), create=True, connSQLServer=connPostgreSQL)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Dump insert model
        insert = functions.to_json(object=product)
        
        # Get next product id
        id = SQLServer.select(conn=connPostgreSQL, query="SELECT nextval('public.product_id_seq') AS id;")[0].get("id")
        
        # Update id
        insert.update({"id": id})
        
        # Update image path
        await functions.save_image(module=auths_per_user.Module.PRODUCT, id=id, image=image, data=insert)
        
        # Insert
        result = SQLServer.insert(conn=connPostgreSQL, query=queries.POSTGRESQL_PRODUCT_INSERT, vars=(insert.get("id"), insert.get("name"), insert.get("description"), insert.get("price"), insert.get("min_quantity"), insert.get("image"), insert.get("id_category"), insert.get("id_institution"), insert.get("id_status")))
        validation = functions.validate_crud_action(result=result, message=messages.INSERT_INTERNAL_SERVER_ERROR, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Commit
        connPostgreSQL.commit()
        
        # Save image
        await functions.save_image(module=auths_per_user.Module.PRODUCT, id=id, image=image, data=insert, save_in_directory=True)
        
        return getJsonResponse(status_code=status.HTTP_201_CREATED, success=True, message="", data=insert)
    except Exception as e:
        print(f"Exception: {e}")
        connPostgreSQL.rollback()
        if (insert):
            if insert.get("image", None) is not None:
                functions.delete_image(image_url=insert.get("image"))
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=messages.EXCEPTION, data={})

def get_products(info: dict[str, Any], connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.SELECT, connSQLServer=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        result = SQLServer.select(connPostgreSQL, query=queries.POSTGRESQL_PRODUCT_SELECT_ALL)
        validation = functions.validate_crud_action(result=result, message=messages.getDataNotFound("Products"), connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = [functions.to_json(object=Product(**row)) for row in result]
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=result)
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def get_product_by_id(info: dict[str, Any], id: PositiveInt, connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.SELECT, connSQLServer=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result = functions.validate_ids(connSQLServer=connPostgreSQL, table=PostgreSQLTables.PRODUCT.value, vars={"id": id})
        validation = functions.validate_crud_action(result=result, message=messages.getDataNotFound("Product"), connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = SQLServer.select(conn=connPostgreSQL, query=queries.POSTGRESQL_PRODUCT_SELECT_BY_ID, vars=(id,))
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=functions.to_json(object=Product(**result[0])))
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def get_products_by_id_institution(info: dict[str, Any], id: PositiveInt, connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.SELECT, connSQLServer=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(connSQLServer=connPostgreSQL, table=PostgreSQLTables.INSTITUTION.value, vars={"id": id})
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = SQLServer.select(conn=connPostgreSQL, query=queries.POSTGRESQL_PRODUCT_SELECT_BY_ID_INSTITUTION, vars=(id,))
        validation = functions.validate_crud_action(result=result, message=messages.getDataNotFound("Products"), connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        result = [functions.to_json(object=Product(**row)) for row in result]
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=result)
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def get_products_by_id_shop(info: dict[str, Any], id_shop: PositiveInt, connPostgreSQL: connection, connMongoDB: MongoClient) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.SELECT, connSQLServer=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(table=PostgreSQLTables.SHOP.value, vars={"id": id_shop}, connSQLServer=connPostgreSQL)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Obtener el stock actual de una tienda
        products = functions.get_product_current_stock(id_shop=id_shop, connPostgreSQL=connPostgreSQL, connMongoDB=connMongoDB)
        validation = functions.validate_crud_action(result=products, message=messages.getDataNotFound("Products"), connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=products)
    except Exception as e:
        print(f"Exception: {e}")
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

async def put_product(*, info: dict[str, Any], product: UpdateProduct, image: UploadFile | None = None, connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.UPDATE, connSQLServer=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result = functions.validate_ids(table=PostgreSQLTables.PRODUCT.value, vars=functions.to_json(object=product), connSQLServer=connPostgreSQL)
        validation = functions.validate_crud_action(result=result, message=result, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Obtener imagen actual
        current_image: str = SQLServer.select(conn=connPostgreSQL, query=queries.POSTGRESQL_PRODUCT_SELECT_BY_ID, vars=(product.id,))[0].get("image")
        
        # Product model dump
        update = functions.to_json(object=product)
        
        # Update image path
        await functions.save_image(module=auths_per_user.Module.PRODUCT, id=product.id, image=current_image if image is None else image, data=update)
        
        # Update product
        result = SQLServer.update(conn=connPostgreSQL, query=queries.POSTGRESQL_PRODUCT_UPDATE, vars=(update.get("name"), update.get("description"), update.get("price"), update.get("min_quantity"), update.get("image"), update.get("id_category"), update.get("id_status"), update.get("id")))
        validation = functions.validate_crud_action(connSQLServer=connPostgreSQL, result=result, message=messages.UPDATE_INTERNAL_SERVER_ERROR)
        if (isinstance(validation, JSONResponse)):
            if update.get("image", None) is not None:
                functions.delete_image(image_url=update.get("image"))
            return validation
        
        # Commit
        connPostgreSQL.commit()
        
        # Delete actual image
        if image is not None and current_image is not None:
            functions.delete_image(image_url=current_image)
        
        # Save image
        if image is not None:
            await functions.save_image(module=auths_per_user.Module.PRODUCT, id=product.id, image=image, data=update, save_in_directory=True)
        
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data=update)
    except Exception as e:
        print(f"Exception: {e}")
        connPostgreSQL.rollback()
        # Delete temp image
        if (update.get("image", None) is not None and "temp-" in update.get("image")):
            functions.delete_image(image_url=update.get("image"))
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def inactivate_product(info: dict[str, Any], id: PositiveInt, connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.UPDATE, connSQLServer=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(table=PostgreSQLTables.PRODUCT.value, vars={"id": id}, connSQLServer=connPostgreSQL)
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Inhabilitar
        result = SQLServer.update(conn=connPostgreSQL, query=queries.POSTGRESQL_PRODUCT_UPDATE_INACTIVATE, vars=(id,))
        validation = functions.validate_crud_action(result=result, message=messages.UPDATE_INTERNAL_SERVER_ERROR, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Commit
        connPostgreSQL.commit()
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data={"id": id})
    except Exception as e:
        print(f"Exception: {e}")
        connPostgreSQL.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})

def activate_product(info: dict[str, Any], id: PositiveInt, connPostgreSQL: connection) -> JSONResponse:
    try:
        # Validar que pueda usar el módulo
        validate = auths_per_user.validate_user_module(id_user=info.get("id"), module=auths_per_user.Module.PRODUCT, crud=auths_per_user.Crud.UPDATE, connSQLServer=connPostgreSQL)
        if (type(validate) == JSONResponse): return validate
        
        # Validar IDs
        result_validate = functions.validate_ids(connSQLServer=connPostgreSQL, table=PostgreSQLTables.PRODUCT.value, vars={"id": id})
        validation = functions.validate_crud_action(result=result_validate, message=result_validate, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Habilitar
        result = SQLServer.update(conn=connPostgreSQL, query=queries.POSTGRESQL_PRODUCT_UPDATE_ACTIVATE, vars=(id,))
        validation = functions.validate_crud_action(result=result, message=messages.UPDATE_INTERNAL_SERVER_ERROR, connSQLServer=connPostgreSQL)
        if (isinstance(validation, JSONResponse)): return validation
        
        # Commit
        connPostgreSQL.commit()
        return getJsonResponse(status_code=status.HTTP_200_OK, success=True, message="", data={"id": id})
    except Exception as e:
        print(f"Exception: {e}")
        connPostgreSQL.rollback()
        return getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=f"There was an error: {str(e)}", data={})
