from pydantic import BaseModel
from pydantic import (
    PositiveInt,
    StrictInt, 
    StrictFloat,
    NaiveDatetime,
    Field
)

class _BaseInventory(BaseModel):
    id_product: StrictInt | None    = Field(title="ID Producto", gt=0)
    id_status: StrictInt | None     = Field(title="ID Producto", gt=0)
    quantity: StrictFloat           = Field(title="Cantidad de stock")

class UpdateInventory(_BaseInventory):
    pass

class _BaseUpdateQuantity(BaseModel):
    id_product: StrictInt | None    = Field(title="ID Producto", gt=0)
    quantity: StrictFloat           = Field(title="Cantidad de stock")

class UpdateInventoryQuantity(_BaseUpdateQuantity):
    pass
