from pydantic import (
 BaseModel,
 EmailStr
)
class Status(BaseModel):
 status: bool

