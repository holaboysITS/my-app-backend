from pydantic import BaseModel, field_validator


class User(BaseModel):
    username: str
    password: str
    
    @field_validator('username')
    def check_name(cls, v):
        
        if v==None or v=='':
            raise ValueError("Lo username non può essere vuoto")
        elif len(v)<6:
            raise ValueError("Lo username deve avere come minimo 6 caratteri")
        elif len(v)>16:
            raise ValueError("Lo username è troppo lungo")
        return v 
    
    @field_validator('password')
    def check_name(cls, v):
        
        if v==None or v=='':
            raise ValueError("La password non può essere vuota")
        return v 
