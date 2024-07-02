from pydantic import BaseModel
from pydantic import (
    PositiveInt,
    PositiveFloat,
    StrictInt,
    StrictStr,
    StrictFloat,
    Field,
    model_validator
)
import json

class _BaseProduct(BaseModel):
    name: StrictStr             = Field(title="Nombre", strict=True)
    description: StrictStr      = Field(title="Descripción", strict=True)
    price: PositiveFloat        = Field(title="Precio", strict=True)
    min_quantity: StrictFloat   = Field(title="Cantidad mínima", strict=True)
    
class _BaseShopIDs(BaseModel):
    id_category: PositiveInt    = Field(title="ID Categoría", strict=True)
    id_institution: PositiveInt = Field(title="ID Institución", strict=True)
    id_status: PositiveInt      = Field(title="ID Status", strict=True)

class Product(_BaseProduct, _BaseShopIDs):
    id: StrictInt | None        = Field(title="ID", ge=0)
    image: StrictStr | None     = Field(title="Imagen", strict=True)

class ProductPerShop(_BaseProduct, _BaseShopIDs):
    id: StrictInt | None        = Field(title="ID", ge=0)
    id_product_shop: StrictInt  = Field(title="ID Producto en tienda", ge=0)
    id_shop: StrictInt | None   = Field(title="ID Tienda", ge=0)
    stock: StrictFloat          = Field(title="Stock", strict=True)
    image: StrictStr | None     = Field(title="Imagen", strict=True)

class CreateProduct(_BaseProduct, _BaseShopIDs):
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class UpdateProduct(_BaseProduct):
    id: StrictInt | None        = Field(title="ID", gt=0)
    id_category: PositiveInt    = Field(title="ID Categoría", strict=True)
    id_status: PositiveInt    = Field(title="ID Categoría", strict=True)
    
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
