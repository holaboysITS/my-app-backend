from pydantic import BaseModel, field_validator

from basemodel.enums.Role import Role

class User(BaseModel):
    username: str
    password: str
    role: Role
    
    @field_validator('username')
    def check_name(cls, v):
        
        if v!=None or v!='':
            raise ValueError("Lo username non può essere vuoto")
        elif len(v)<6:
            raise ValueError("Lo username deve avere come minimo 6 caratteri")
        elif len(v)>16:
            raise ValueError("Lo username è troppo lungo")
        return v 
    
    @field_validator('password')
    def check_name(cls, v):
        
        if v!=None:
            raise ValueError("Non trovo il nome")
        return v 
