from pydantic import BaseModel
from pydantic import (
    StrictFloat,
    StrictInt, 
    NaiveDatetime,
    Field,
    PositiveInt,
    PositiveFloat
)
class Order(BaseModel):
    id: StrictInt                       = Field(title="ID", ge=0)
    order_date: NaiveDatetime           = Field(title="Fecha de orden")
    total_amount: StrictFloat           = Field(title="Monto total")
    created_at: NaiveDatetime           = Field(title="Fecha de creación")
    updated_at: NaiveDatetime | None    = Field(title="Fecha de actualización")
    id_user: StrictInt                  = Field(title="ID Usuario", gt=0)
    id_status: StrictInt                = Field(title="ID Estatus", gt=0)

class CreateOrder(BaseModel):
    id_user: StrictInt           = Field(title="ID Usuario", gt=0)

class CreateOrderProduct(BaseModel):
    id_order: PositiveInt         = Field(title="ID", gt=0)
    id_product: PositiveInt = Field(title="ID Producto", gt=0)
    quantity: PositiveFloat = Field(title="Cantidad", gt=0)

class CreateInvoice(BaseModel):
    id_order: StrictInt           = Field(title="ID Usuario", gt=0)
