from pydantic import BaseModel
from pydantic import (
    StrictStr,
    PositiveInt,
    Field
)

class _BaseCategory(BaseModel):
    id: PositiveInt     = Field(title="ID Categoría")
    name: StrictStr     = Field(title="Nombre categoría")

class Category(_BaseCategory):
    pass
