from bson import ObjectId
from pydantic import BaseModel, Field,field_validator
from typing import Optional,Annotated
# from enums import Status

class Machinery(BaseModel):
    # id: Optional[ObjectId] = Field(alias="_id", default=None)
    plant_id: int 
    
    name : str
    type : str
    # status : Status
    specifications : dict
    
    @field_validator('name')
    def check_name(cls, v):
        
        if v==None or v=='':
            raise ValueError("Non trovo il nome")
        return v    
    
    @field_validator('type')
    def check_name(cls, v):
        
        if v==None or v=='':
            raise ValueError("Non trovo il tipo")
        return v
    
    # @field_validator('status')
    # def check_name(cls, v):
        
        if v==None or v=='':
            raise ValueError("Non capisco in che stato sia")
        return v
    
    @field_validator('specifications')
    def check_name(cls, v):
        
        if v==None or v=='':
            raise ValueError("Non trovo le specifiche")
        return v