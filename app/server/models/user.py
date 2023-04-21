from typing import Optional, Union
from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    username: str=Field(...)
    email: str=Field(...)
    full_name: str=Field(...)
    hashed_password: str=Field(...)
    disabled: bool
    class Config:
        orm_mode=True
        schema_example = {
            "example": {
                "username": "Valid username",
                "email": "Valid email of the user",
                "full_name": "Full Name of the User",
                "hashed_password": "Encoded password",
                "disabled": False,
            }
        }

class UpdateUserModel(BaseModel):
    username: Optional[str]
    full_name: Optional[str]
    disabled: Optional[str]

class ChangePassword(BaseModel):
    username: str=Field(...)
    old_password: str=Field(...)
    new_password: str=Field(...)

class Token(BaseModel):
    access_token: str=Field(...)
    token_type: str=Field(...)

class TokenData(BaseModel):
    username: Optional[str]

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