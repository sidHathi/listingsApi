from pydantic import BaseModel, Field

class Error(BaseModel):
    errorCode: str = Field(
        description='Error enumerator',
        example='UUID_NOT_FOUND'
    )
    errorMessage: str = Field(
        description='English language description of the error',
        example='No listing found for provided uuid'
    )