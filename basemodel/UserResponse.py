from pydantic import BaseModel, field_validator


class UserResponse(BaseModel):
    username: str

    
    
