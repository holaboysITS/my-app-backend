from dataclasses import Field
from enum import Enum
from typing import Annotated, Optional
from requests import Session, session
from bson import ObjectId
from pydantic import BaseModel, field_validator, validator

from basemodel.Machinery import Machinery     

class Plant(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id", default=None)
    name: str
    location: str
    description: str
    machineries: list[str]

    @field_validator('name')
    def name_validator(cls, value):
        if not value:
            raise ValueError('Si deve specificare il nome')
        elif len(value) < 3:
            raise ValueError('Il nome deve essere più lungo di 3 caratteri')
        #L'ho trovato su internet, però non so se funziona
        existing_name = session.query(Plant).filter_by(name=value).first()
        if existing_name:
            raise ValueError('Il nome deve essere unico e non può già esistere nel database')
 
        return value

    @field_validator('location')
    def location_validator(cls, value):
        if not value:
            raise ValueError('Si deve specificare la posizione.')
        return value

    @field_validator('description')
    def validate_description(cls, value):
        if not value:
            raise ValueError('Si deve mettere qualche descrizione.')
        elif len(value) > 500:
            raise ValueError('La descrizione non deve essere più lunga di 500 caratteri')
        return value

#L'ho trovato su internet, però non so se funziona
    @validator('machineries')
    def validate_machineries(cls, machineries, values, config, field):
        session: Session = values.get('session')  # Assuming session is passed in values
        if not session:
            raise ValueError("Sessione del database non fornita.")

        for machinery_name in machineries:
            existing_machinery = session.query(Machinery).filter_by(name=machinery_name).first()
            if not existing_machinery:
                raise ValueError(f"La macchina '{machinery_name}' non esiste nel database.")
        
        return machineries
