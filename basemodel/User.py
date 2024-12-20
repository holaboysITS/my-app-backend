from pydantic import BaseModel, field_validator
from enum import Enum


class User(BaseModel):
    username: str
    password: str
    
    @field_validator('username')
    def check_username(cls, v):
        
        if v==None or v=='':
            raise ValueError("Lo username non può essere vuoto")
        elif len(v)<5:
            raise ValueError("Lo username deve avere come minimo 6 caratteri")
        elif len(v)>16:
            raise ValueError("Lo username è troppo lungo")
        return v 
    
    @field_validator('password')
    def check_password(cls, v):
        
        if v==None or v=='':
            raise ValueError("La password non può essere vuota")
        return v 
