from pydantic import BaseModel, field_validator
from enum import Enum


class Role(str, Enum):
    admin = 'admin'
    operator = 'operator'

class User(BaseModel):
    username: str
    password: str
    role: Role

class UserResponse(BaseModel):
    username: str
    role: Role
