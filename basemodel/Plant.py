from dataclasses import Field
from bson import ObjectId
from typing import Optional
from requests import session
from pydantic import BaseModel, field_validator     

class Plant(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id", default=None)
    name: str
    location: str
    description: str
    machineries: list[str]
