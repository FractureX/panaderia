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
from src.shared.infrastructure.database.mongodb import MongoDB
from src.shared.infrastructure.database.sqlserver import SQLServer
from src.auth.utils.functions.functions import validate_token

router = APIRouter()

@router.post("/add", response_model=CustomResponse, name="Add product")
async def post_product(product: CreateProduct = Body(...), image: Optional[UploadFile] = File(None), info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return await service.post_product(info=info, product=product, image=image, connPostgreSQL=connPostgreSQL)

@router.get("/", response_model=CustomResponses, name="Get all products")
async def get_products(info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_products(info=info, connPostgreSQL=connPostgreSQL)

@router.get("/product/{id}", response_model=CustomResponse, name="Get product by id")
async def get_product_by_id(id: PositiveInt, info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_product_by_id(info=info, connPostgreSQL=connPostgreSQL, id=id)

@router.get("/institution/{id_institution}", response_model=CustomResponses, name="Get product by id institution")
async def get_products_by_id_institution(id_institution: PositiveInt, info: dict[str, Any] = Depends(validate_token), connPostgreSQ: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_products_by_id_institution(info=info, id=id_institution, connPostgreSQL=connPostgreSQ)

@router.get("/shop/{id_shop}", response_model=CustomResponses, name="Get product by id shop")
async def get_products_by_id_shop(id_shop: PositiveInt, info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection), connMongoDB: MongoClient = Depends(MongoDB.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_products_by_id_shop(info=info, id_shop=id_shop, connPostgreSQL=connPostgreSQL, connMongoDB=connMongoDB)

@router.put("/modify", response_model=CustomResponse, name="Modify product")
async def put_product(product: UpdateProduct = Body(...), image: Optional[UploadFile] = File(None), info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return await service.put_product(info=info, product=product, image=image, connPostgreSQL=connPostgreSQL)

@router.delete("/inactivate/{id}", response_model=CustomResponse, name="Inactivate product")
async def inactivate_product(id: PositiveInt, info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.inactivate_product(info=info, id=id, connPostgreSQL=connPostgreSQL)

@router.put("/activate/{id}", response_model=CustomResponse, name="Activate product")
async def activate_product(id: PositiveInt, info: dict[str, Any] = Depends(validate_token), connPostgreSQL: connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.activate_product(info=info, id=id, connPostgreSQL=connPostgreSQL)
