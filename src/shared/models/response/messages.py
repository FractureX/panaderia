EXCEPTION = "Hubo una excepción"

USER_NO_ACTIVE = "Usuario sin estatus activo"
USER_DELETE_SAME_USER = "No se puede borrar el mismo usuario"
USER_UPDATE_INACTIVATE_SAME_USER = "No se puede desactivar el mismo usuario"
USER_UPDATE_ACTIVATE_SAME_USER = "No se puede activar el mismo usuario"

CREDENTIALS_EXPIRED_SIGNATURE = "Token expirado"
CREDENTIALS_INVALID = "Credenciales inválidas"
CREDENTIALS_COULD_NOT_VALIDATE = "No se pudo validar las credenciales"

NO_DATA_ROLE = "Sin data en rol"

IMAGE_DIRECTORY_NOT_FOUND = "Image directory not found"

def getDataNotFound(dataName: str) -> str:
    return f"{dataName} no encontrado"

def getDataAlreadyExists(dataName: str) -> str:
    return f"El valor '{dataName}' ya existe"

SELECT_INTERNAL_SERVER_ERROR = "Hubo un problema seleccionando información"
INSERT_INTERNAL_SERVER_ERROR = "Hubo un problema insertando información"
UPDATE_INTERNAL_SERVER_ERROR = "Hubo un problema actualizando información"
DELETE_INTERNAL_SERVER_ERROR = "Hubo un problema eliminando información"