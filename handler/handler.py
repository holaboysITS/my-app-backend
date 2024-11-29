from fastapi import APIRouter, HTTPException, Body, status, Query
from bson import ObjectId
from db import user_collection, machinery_collection, plant_collection
from basemodel.Plant import Plant, PlantResponse, PlantResponse2
from basemodel.Machinery import Machinery, MachineryEdit, MachineryResponse
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


#GET UN IMPIANTO
@router.get(
    "/plants/{plant_id}",
    response_description="prendi un impianto",
    response_model=Plant,
    response_model_by_alias=False,
)
async def show_plant(id: str):
    if (
        plant := plant_collection.find_one({"_id": ObjectId(id)}) #walrus operator, if a variable is present, then it uses it TRUST ME :)
    ) is not None:
        return plant
    raise HTTPException(status_code=404, detail=f"Impianto {id} not found")


#GET LIST DEGLI IMPIANTI
@router.get(
    "/plants",
    response_description="List all plants",
    response_model=List[PlantResponse],
    response_model_by_alias=True,
)
async def list_plants():
    plants = plant_collection.find().to_list(1000)
    for plant in plants:
        plant["_id"] = str(plant["_id"])

    # for plant in plants:
    #     plant["machineries"] = [await get_machineries_by_id(i) for i in plant["machineries"]]

    return plants


#PUT DI UN IMPIANTO
@router.put(
        "/plants/{plant_id}",
    response_description="modifica impianto",
    response_model= PlantResponse,
    #response_model_by_alias=False,
)
async def update_plant(plant_id: str, plant: Plant ):

    plant = {
        k: v for k, v in plant.model_dump().items() if v is not None
    }
    
    updated_plant = plant_collection.update_one(
                {"_id": ObjectId(plant_id)},
                {"$set": plant},
            ) 
    if updated_plant.modified_count == 1:
    
        updated_plant_db = plant_collection.find_one({"_id":ObjectId(plant_id)})
        updated_plant_db["_id"] = str(updated_plant_db['_id'])

        return PlantResponse(**updated_plant_db)
    
    raise HTTPException(status_code=404, detail=f"Impianto {plant_id} not found")

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

#Get by id Machinery
@router.get("/machineries/{machinery_id}", response_model=Machinery)
async def get_machineries_by_id(machinery_id: str):
    # Convert plant_id from string to ObjectId
    try:
        machinery_id = ObjectId(machinery_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    # Query the plant collection by _id
    machinery = machinery_collection.find_one({"_id": machinery_id})
    
    if machinery is None:
        raise HTTPException(status_code=404, detail="Machinary not found")
    
    # Convert ObjectId to string for the response
    machinery["id"] = str(machinery["_id"])  # MongoDB returns _id, we want id in response
    del machinery["_id"]  # Optionally remove the _id field if you only want the 'id'
    
    return machinery


#GET LIST PLANT MACHINARIES
@router.get(
    "/machineries/{plant_id}/plant",
    response_description="List all machineries from a plant",
    response_model=List[Machinery],
    response_model_by_alias=True,
)
async def list_machineries(plant_id: str):
    
    try:
        plant_id_format = ObjectId(plant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    machineries = machinery_collection.find({"plant_id": plant_id}).to_list(1000)

    if not machineries:
        raise HTTPException(status_code=404, detail="Patatina")
    return machineries

#PUT MACHINARY
@router.put(
        "/machinery/{machinery_id}",
    response_description="modifica macchinario",
    response_model= MachineryResponse,
    #response_model_by_alias=False,
)
async def update_machinery(machinery_id: str, machinery: MachineryEdit ):

    machinery = {
        k: v for k, v in machinery.model_dump().items() if v is not None
    }
    
    updated_machinery = machinery_collection.update_one(
                {"_id": ObjectId(machinery_id)},
                {"$set": machinery},
            ) 
    
    if updated_machinery.modified_count == 1:
    
        updated_machinery_db = machinery_collection.find_one({"_id":ObjectId(machinery_id)})
        updated_machinery_db["_id"] = str(updated_machinery_db['_id'])
    
        return MachineryResponse(**updated_machinery_db)

#All Macchinari
@router.get(
    "/machineries",
    response_description="List of all machineries",
    response_model=List[MachineryResponse],
    response_model_by_alias=True,
)
async def list_machineries():
    machineries = machinery_collection.find().to_list(1000)
    for machinery in machineries:
        machinery["_id"] = str(machinery["_id"])  
    return machineries
#Delete all P
@router.delete("/plants" , status_code=status.HTTP_200_OK)
def delete_plant():
    plants = plant_collection.find().to_list(1000)
    for plant in plants:
        plant_collection.find_one_and_delete(plant)
    
    return {"message": "Plant deleted successfully"}
#Delete all M
@router.delete("/machinaries" , status_code=status.HTTP_200_OK)
def delete_machinery():
    machinerys = machinery_collection.find().to_list(1000)
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



@router.delete("/deleteMachinariesById/{machinery_id}" , status_code=status.HTTP_200_OK)
def delete_machinery(machinery_id: str):
    machinery = machinery_collection.find_one({"_id": ObjectId(machinery_id)})
    if machinery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machinery not found")
    
    plant_id = machinery['plant_id']

    deleted = machinery_collection.delete_one({"_id": ObjectId(machinery_id)})
    if deleted.deleted_count == 1:
        if plant_id:
            plant_collection.update_one(
                {'_id': ObjectId(plant_id)},
                {'$pull': {'machinery': machinery_id}}
            )
        return {"message": "Machinery with ID: {} deleted successfully".format(machinery_id)}
    else:
        raise HTTPException(status_code=404, detail="errore che non so")



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

@router.get(
    "/allUser",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    response_model_by_alias=True,
    ) #DO NOT IMPLEMENT IN FRONTEND
def get_all_users():

    result: List[UserResponse] = list(user_collection.find())

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users registered and we don't even have a registration form so we basically have to ask our db admin to put some more users in")
    return result






    
    
    