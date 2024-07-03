from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from typing import Any
import pyodbc

from src.order.domain.models import (
    CreateOrder,
    CreateOrderProduct,
    CreateInvoice
)
from src.order.infrastructure import service
from src.shared.models.response.response import (
    CustomResponse,
    CustomResponses
)
from src.shared.infrastructure.database.sqlserver import SQLServer
from src.auth.utils.functions.functions import validate_token

router = APIRouter()

@router.post("/add", response_model=CustomResponse, name="Add order")
async def post_order(order: CreateOrder, info: dict[str, Any] = Depends(validate_token), connSQLServer: pyodbc.Connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.post_order(info=info, order=order, connSQLServer=connSQLServer)

@router.get("/", response_model=CustomResponses, name="Get all orders")
async def get_orders(info: dict[str, Any] = Depends(validate_token), connSQLServer: pyodbc.Connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_orders(info=info, connSQLServer=connSQLServer)

@router.get("/{id}", response_model=CustomResponse, name="Get order by id")
async def get_order_by_id(id: PositiveInt, info: dict[str, Any] = Depends(validate_token), connSQLServer: pyodbc.Connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.get_order_by_id(info=info, id=id, connSQLServer=connSQLServer)

@router.post("/product/add", response_model=CustomResponse, name="Add order item")
async def post_order_product(order: CreateOrderProduct, info: dict[str, Any] = Depends(validate_token), connSQLServer: pyodbc.Connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.post_order_product(info=info, order=order, connSQLServer=connSQLServer)

@router.post("/invoice/add", response_model=CustomResponse, name="Add invoice")
async def post_invoice(order: CreateInvoice, info: dict[str, Any] = Depends(validate_token), connSQLServer: pyodbc.Connection = Depends(SQLServer.get_connection)):
    if (type(info) == JSONResponse): return info
    return service.post_invoice(info=info, order=order, connSQLServer=connSQLServer)
