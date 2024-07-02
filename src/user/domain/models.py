from pydantic import BaseModel
from pydantic import (
    StrictStr,
    EmailStr,
    StrictInt, 
    NaiveDatetime,
    Field
)
class _BaseUser(BaseModel):
    username: StrictStr                 = Field(title="Nombre", strict=True)
    password: StrictStr                 = Field(title="Apellido", strict=True)
    email: EmailStr                     = Field(title="Correo", strict=True)
    id_role: StrictInt                  = Field(title="ID Rol", strict=True, gt=0)
    id_status: StrictInt                = Field(title="ID Estatus", strict=True, gt=0)

class User(_BaseUser):
    id: StrictInt | None                = Field(title="ID", ge=0)
    created_at: NaiveDatetime           = Field(title="Fecha de creación")
    updated_at: NaiveDatetime | None    = Field(title="Fecha de actualización")

class CreateUser(_BaseUser):
    pass

class UpdateUser(_BaseUser):
    id: StrictInt | None                = Field(title="ID", ge=0)
    pass
