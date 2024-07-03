from fastapi import APIRouter, Depends, File, UploadFile, Body
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from pymongo import MongoClient
from psycopg2.extensions import connection
from typing import (
    Optional,
    Any
)

from src.product.domain.models import (
    CreateProduct,
    UpdateProduct
)
from src.product.infrastructure import service
from src.shared.models.response.response import (
    CustomResponse,
    CustomResponses
)
from src.shared.infrastructure.database.sqlserver import SQLServer
from src.auth.utils.functions.functions import validate_token

router = APIRouter()

@router.post("/add", response_model=CustomResponse, name="Add product")
async def post_product(product: CreateProduct = Body(...), image: Optional[UploadFile] = File(None), info: dict[str, Any] = Depends(validate_token), connSQLServer: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return await service.post_product(info=info, product=product, image=image, connSQLServer=connSQLServer)

@router.get("/", response_model=CustomResponses, name="Get all products")
async def get_products(info: dict[str, Any] = Depends(validate_token), connSQLServer: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_products(info=info, connSQLServer=connSQLServer)

@router.get("/{id}", response_model=CustomResponse, name="Get product by id")
async def get_product_by_id(id: PositiveInt, info: dict[str, Any] = Depends(validate_token), connSQLServer: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_product_by_id(info=info, id=id, connSQLServer=connSQLServer)

@router.get("/category/{id_category}", response_model=CustomResponse, name="Get product by id category")
async def get_product_by_id_category(id_category: PositiveInt, info: dict[str, Any] = Depends(validate_token), connSQLServer: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_product_by_id_category(info=info, id_category=id_category, connSQLServer=connSQLServer)

@router.put("/modify", response_model=CustomResponse, name="Modify product")
async def put_product(product: UpdateProduct = Body(...), image: Optional[UploadFile] = File(None), info: dict[str, Any] = Depends(validate_token), connSQLServer: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return await service.put_product(info=info, product=product, image=image, connSQLServer=connSQLServer)

@router.delete("/delete/{id}", response_model=CustomResponse, name="Delete product")
async def inactivate_product(id: PositiveInt, info: dict[str, Any] = Depends(validate_token), connSQLServer: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.delete_product(info=info, id=id, connSQLServer=connSQLServer)
