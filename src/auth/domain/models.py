from pydantic import BaseModel
from pydantic import (
    StrictStr,
    StrictInt, 
    EmailStr,
    PositiveInt, 
    Field
)

class Credential(BaseModel):
    id: StrictInt | None    = Field(title="ID", ge=0)
    email: EmailStr         = Field(title="Email", strict=True)
    password: StrictStr     = Field(title="Contraseña", strict=True)

class CreateCredential(BaseModel):
    password: StrictStr     = Field(title="Password", strict=True)

class UpdateCredential(CreateCredential):
    pass

class Auth(BaseModel):
    name: StrictStr                     = Field(title="Nombre", strict=True)
    role: StrictStr                     = Field(title="Rol", strict=True)
    access_token: StrictStr             = Field(title="Token de acceso", strict=True)
    token_type: StrictStr               = Field(title="Tipo de token", default="bearer", strict=True)
    id_user: PositiveInt                = Field(title="ID Usuario", strict=True)
    id_institution: PositiveInt | None  = Field(title="ID Institución", strict=True)
