from typing import Optional
from fastapi.responses import JSONResponse
from typing import Union
from pydantic import (
    StrictStr, 
    PositiveInt, 
    StrictBool, 
    BaseModel
)

class BaseResponse(BaseModel):
    status_code: PositiveInt
    success: StrictBool
    message: StrictStr

class CustomResponse(BaseResponse):
    data: dict

class CustomResponses(BaseResponse):
    data: list[dict]
    
@staticmethod
def getJsonResponse(status_code: int, success: bool, message: str, data: Union[dict, list], headers: dict[str, str] = None) -> JSONResponse:
    return JSONResponse(
        headers=headers,
        status_code=status_code,
        content={
            "success": success,
            "message": message, 
            "data": data
        }
    )
