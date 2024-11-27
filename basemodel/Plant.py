from dataclasses import Field
from enum import Enum
from typing import Annotated, Optional
from requests import session
from models import Machinery
from pydantic import BaseModel, field_validator     

PyObjectId = int 

class Plant(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    location: str
    description: str
    machineries: list[str]

    @field_validator('name')
    def name_validator(cls, value):
        if not value:
            raise ValueError('Name must not be empty')
        elif len(value) < 3:
            raise ValueError('Name must be at least 3 characters long')
        
        existing_plant = session.query(Plant).filter_by(name=value).first()
        if existing_plant:
            raise ValueError('Il nome deve essere unico e non può già esistere nel database')
 
        return value

    @field_validator('location')
    def location_validator(cls, value):
        if not value:
            raise ValueError('Location must not be empty')
        return value

    @field_validator('description')
    def validate_description(cls, value):
        if not value:
            raise ValueError('Description must not be empty')
        elif len(value) > 500:
            raise ValueError('Name must be at least 3 characters long')
        return value

