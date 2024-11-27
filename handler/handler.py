from fastapi import APIRouter, HTTPException, Body, status
from basemodel import User, Plant, Machinery
from pydantic import BaseModel
from db import user_collection, machinery_collection, plant_collection

router = APIRouter()

#POST DEGLI UTENTI
@router.post(
    "/user",
    response_description="Add new user",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
def create_user(user: User = Body(...)):

    new_user = user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user

#POST DEI MACCHINARI
@router.post(
    "/machinery",
    response_description="Add new machinery",
    response_model=Machinery,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
def create_machinery(machinery: Machinery = Body(...)):

    new_machinery = machinery_collection.insert_one(
        machinery.model_dump(by_alias=True, exclude=["id"])
    )
    created_machinery = machinery_collection.find_one(
        {"_id": new_machinery.inserted_id}
    )
    return created_machinery


#POST DEGLI IMPIANTI
@router.post(
    "/plant",
    response_description="Add new plant",
    response_model=Plant,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
def create_plant(plant: Plant = Body(...)):

    new_plant = plant_collection.insert_one(
        plant.model_dump(by_alias=True, exclude=["id"])
    )
    created_plant = plant_collection.find_one(
        {"_id": new_plant.inserted_id}
    )
    return created_plant
