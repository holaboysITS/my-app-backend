from fastapi import APIRouter, HTTPException, Body, status, Query
from bson import ObjectId
from db import user_collection, machinery_collection, plant_collection
from basemodel.Plant import Plant, PlantResponse
from basemodel.Machinery import Machinery, MachineryResponse, MachineryInput
from basemodel.UserResponse import UserResponse
from basemodel.User import User
from typing import List

router = APIRouter()

# Utility function to convert MongoDB ObjectId to str
def convert_objectid_to_str(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)  # Convert ObjectId to string
    return data

# POST DI UN IMPIANTO
@router.post(
    "/plants",
    response_description="Add new plant",
    response_model=Plant,
    status_code=status.HTTP_200_OK,
)
async def create_plant(plant: Plant = Body(...)):
    new_plant = plant_collection.insert_one(
        plant.model_dump(exclude=["id"], by_alias=True,)  # Exclude 'id' for insertion
    )
    created_plant = plant_collection.find_one({"_id": new_plant.inserted_id})
    return created_plant


#GET LIST DEGLI IMPIANTI
@router.get(
    "/plants",
    response_description="List all plants",
    response_model=List[PlantResponse],
    response_model_by_alias=True,
)
async def list_plants():
    plants = list(plant_collection.find().to_list(1000))
    for plant in plants:
        plant["_id"] = str(plant["_id"])  
    return plants

# Post Machinery
@router.post(
    "/machineries",
    response_description="Add new machinery",
    response_model=Machinery,
    status_code=status.HTTP_200_OK,
)
async def create_machinery(machinery: Machinery = Body(...)):
    new_machinery = machinery_collection.insert_one(
        machinery.model_dump(exclude=["id"], by_alias=True)  # Exclude 'id' for insertion
    )
    created_machinery = machinery_collection.find_one({"_id": new_machinery.inserted_id})
    
    plant_collection.update_one(
        {"_id":ObjectId(machinery.plant_id)},
        {"$push": {"machineries": str(new_machinery.inserted_id)}}
    )
    return created_machinery


#GET LIST DEI MACCHINARI DI UN IMPIANTO
@router.get(
    "/machineries/{plant_id}",
    response_description="List all machineries from a plant",
    response_model=List[MachineryResponse],
    response_model_by_alias=True,
)
async def list_machineries(plant_id: str):
    machineries = list(machinery_collection.find({"plant_id": plant_id}).to_list(1000))
    for machinery in machineries:
        machinery["_id"] = str(machinery["_id"])  
    return machineries

#All Macchinari
@router.get(
    "/machineries",
    response_description="List of all machineries",
    response_model=List[MachineryResponse],
    response_model_by_alias=True,
)
async def list_machineries():
    machineries = list(machinery_collection.find().to_list(1000))
    for machinery in machineries:
        machinery["_id"] = str(machinery["_id"])  
    return machineries
#Delete all P
@router.delete("/plants" , status_code=status.HTTP_200_OK)
def delete_plant():
    plants = list(plant_collection.find().to_list(1000))
    for plant in plants:
        plant_collection.find_one_and_delete(plant)
    
    return {"message": "Plant deleted successfully"}
#Delete all M
@router.delete("/machinaries" , status_code=status.HTTP_200_OK)
def delete_machinery():
    machinerys = list(machinery_collection.find().to_list(1000))
    for machinery in machinerys:
        machinery_collection.find_one_and_delete(machinery)
    
    return {"message": "Plant deleted successfully"}

@router.delete("/plants/{plant_id}" , status_code=status.HTTP_200_OK)
def delete_plant(plant_id: str):
    plant = plant_collection.find_one({"_id": ObjectId(plant_id)})
    if plant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")
    plant_collection.delete_one({"_id": ObjectId(plant_id)})
    return {"message": "Plant with ID: {} deleted successfully".format(plant_id)}



@router.delete("/machinaries/{machinery_id}" , status_code=status.HTTP_200_OK)
def delete_machinery(machinery_id: str):
    machinery = machinery_collection.find_one({"_id": ObjectId(machinery_id)})
    if machinery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machinery not found")
    machinery_collection.delete_one({"_id": ObjectId(machinery_id)})
    return {"message": "Machinery with ID: {} deleted successfully".format(machinery_id)}



# # POST Route to create new machinery
@router.post(
    "/plants/{plants_id}/machinery",
    response_description="Add new machinery",
    response_model=Machinery,
    status_code=status.HTTP_200_OK,
)
def create_machinery(machinery: Machinery = Body(...)):
    new_machinery = machinery_collection.insert_one(
        machinery.model_dump(exclude=["id"], by_alias=True)  # Exclude 'id' for insertion
    )
    created_machinery = machinery_collection.find_one({"_id": new_machinery.inserted_id})
    return created_machinery


# # GET Route to list all plants (asynchronous)
# # @router.get(
# #     "/plants",
# #     response_description="List all plants",
# #     response_model=list[Plant],  # List of Plant models
# # )
# async def list_plants():
#     plants = await plant_collection.find().to_list(1000)  # Retrieve up to 1000 plants
#     return [convert_objectid_to_str(plant) for plant in plants]  # Convert ObjectId to str for each plant

# GET Route to read a specific user by username and password
@router.post("/user/", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read_user(input: User):

    username = input.username
    password = input.password
    user = user_collection.find_one({"username": username, "password": password})
    user = convert_objectid_to_str(user)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    response = UserResponse(username=user['username'])
    
    return response




    
    
    