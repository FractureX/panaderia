from pydantic import BaseModel
from pydantic import (
    StrictStr,
    EmailStr,
    StrictInt, 
    StrictFloat,
    Field
)
from enum import Enum

from src.auth.domain.models import (
    Credential,
    CreateCredential,
    UpdateCredential
)

class Gender(str, Enum):
    MALE    = "Male"
    FEMALE  = "Female"
    OTHER   = "Other"
    
    @classmethod
    def _missing_(cls, value):
        if value.lower() == "male":
            return cls.MALE
        elif value.lower() == "female":
            return cls.FEMALE
        elif value.lower() == "other":
            return cls.OTHER
    
class _BaseUser(BaseModel):
    name: StrictStr                     = Field(title="Nombre", strict=True)
    surname: StrictStr                  = Field(title="Apellido", strict=True)
    email: EmailStr                     = Field(title="Correo", strict=True)
    gender: Gender                      = Field(title="Género")
    id_status: StrictInt                = Field(title="ID Estatus", strict=True, gt=0)
    id_role: StrictInt                  = Field(title="ID Rol", strict=True, gt=0)
    id_shop: StrictInt | None           = Field(title="ID Vendedor", strict=True, gt=0)
    id_institution: StrictInt | None    = Field(title="ID Institución", strict=True, gt=0)

class User(_BaseUser):
    id: StrictInt | None        = Field(title="ID", ge=0)
    credits: StrictFloat        = Field(title="Créditos", strict=True, default=0, ge=0)
    credential: Credential

class CreateUser(_BaseUser):
    credential: CreateCredential

class UpdateUser(_BaseUser):
    id: StrictInt | None        = Field(title="ID", ge=0)
    credential: UpdateCredential | None = None

class SearchUserClientInstitutionCriteria(BaseModel):
    id_institution: StrictInt   = Field(title="ID Institución", strict=True, gt=0)
    criteria: StrictStr         = Field(title="Criterio a buscar", strict=True)
