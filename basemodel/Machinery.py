from bson import ObjectId
from pydantic import BaseModel, Field,field_validator
from typing import Optional,Annotated
from basemodel.enums.Status import Status
from db import user_collection, machinery_collection, plant_collection

class MachineryResponse(BaseModel):
    id: str = Field(alias="_id", default=None)
    plant_id: str
    
    name : str
    type : str
    status : Status
    specifications : Optional[dict] = {}
    
class Machinery(BaseModel):
    plant_id: str
    name : str
    type : str
    status : Status
    specifications : Optional[dict] = {}
        

    
    @field_validator('name')
    def check_name(cls, v):
        
        if v==None or v=='':
            raise ValueError("Non trovo il nome")
        return v    
    
    @field_validator('type')
    def check_type(cls, v):
        
        if v==None or v=='':
            raise ValueError("Non trovo il tipo")
        return v
    
    @field_validator('status')
    def check_status(cls, v):
        
        if v==None or v=='':
            raise ValueError("Non capisco in che stato sia")
        return v
    
    @field_validator('specifications')
    def check_specifications(cls, v):
        
        if v==None or v=='':
            raise ValueError("Non trovo le specifiche")
        return v
    
class MachineryEdit(BaseModel):
    plant_id: Optional[str] = None 
    name: Optional[str] = None 
    type: Optional[str] = None
    status: Optional[Status] = None
    specifications: Optional[dict] = {}