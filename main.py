import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Config, Server

from src.shared.config.Environment import get_environment_variables
from src.auth.application.router import router as auth_router
from src.user.application.router import router as user_router
from src.product.application.router import router as product_router
from src.inventory.application.router import router as inventory_router
from src.category.application.router import router as category_router
from src.order.application.router import router as order_router
from src.shared.utils.functions.auth import get_password_hash

# Environments variables
_environmentVariables = get_environment_variables()

app = FastAPI(
    title=_environmentVariables.APP_NAME,
    version=_environmentVariables.API_VERSION,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Routers
app.include_router(router=auth_router, prefix="/token", tags=["auth"])
app.include_router(router=category_router, prefix="/category", tags=["category"])
app.include_router(router=product_router, prefix="/product", tags=["product"])
app.include_router(router=inventory_router, prefix="/inventory", tags=["inventory"])
app.include_router(router=user_router, prefix="/user", tags=["user"])
app.include_router(router=order_router, prefix="/order", tags=["order"])

os.makedirs(os.getcwd() + os.sep + "images" + os.sep + "PRODUCT", exist_ok=True)

print(get_password_hash("123456"))

if __name__ == "__main__":
    Server(Config(app="main:app", reload=True)).run()
