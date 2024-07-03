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
    
class _BaseShopIDs(BaseModel):
    id_category: PositiveInt    = Field(title="ID Categoría", strict=True)
    id_status: PositiveInt      = Field(title="ID Status", strict=True)

class Product(_BaseProduct, _BaseShopIDs):
    id: StrictInt | None        = Field(title="ID", ge=0)
    image: StrictStr | None     = Field(title="Imagen", strict=True)
    quantity: StrictFloat       = Field(title="Stock", strict=True)

class CreateProduct(_BaseProduct, _BaseShopIDs):
    quantity: PositiveFloat    = Field(title="Stock del producto")
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class UpdateProduct(_BaseProduct, _BaseShopIDs):
    id: StrictInt | None        = Field(title="ID", gt=0)
    
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
