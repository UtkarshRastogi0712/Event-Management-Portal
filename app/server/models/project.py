from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class Item(BaseModel):
    name: str
    price: float
    quantity: int
    category: Optional[Literal['Construction','Electrical','Plumbing','Labour','Flooring and Tiling','Miscellaneous']]

class ProjectSchema(BaseModel):
    name: str=Field(...)
    start_date: datetime
    creator: str
    description: str=Field(...)
    items: Optional[list[Item]] = None
    access: Optional[list[str]] = None
    class Config:
        orm_mode=True
        schema_example = {
            "example": {
                "name": "Something",
                "start_date": "Something",
                "creator": "Something",
                "description": "Something",
            }
        }

class UpdateProjectModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    access: Optional[list[str]] = None

def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message
    }

def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }