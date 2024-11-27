from pydantic import BaseModel, field_validator

from basemodel.enums.Role import Role

class UserResponse(BaseModel):
    username: str
    role : Role
    
    
