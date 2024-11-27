from fastapi import APIRouter, HTTPException, Body, status, Query
from bson import ObjectId
from db import user_collection, machinery_collection, plant_collection
from basemodel import User, Plant, Machinery
from basemodel.User import User, UserResponse

router = APIRouter()

# Utility function to convert MongoDB ObjectId to str
def convert_objectid_to_str(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)  # Convert ObjectId to string
    return data

# # POST Route to create a new user
# @router.post(
#     "/user",
#     response_description="Add new user",
#     response_model=User,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_user(user: User = Body(...)):
#     # Remove 'id' field from user model as it's auto-generated by MongoDB
#     new_user = user_collection.insert_one(
#         user.dict(exclude={"id"})  # Ensure 'id' is not included in the insert
#     )
#     created_user = user_collection.find_one({"_id": new_user.inserted_id})
#     return convert_objectid_to_str(created_user)  # Convert ObjectId to str before returning

# # POST Route to create new machinery
# @router.post(
#     "/machinery",
#     response_description="Add new machinery",
#     response_model=Machinery,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_machinery(machinery: Machinery = Body(...)):
#     new_machinery = machinery_collection.insert_one(
#         machinery.dict(exclude={"id"})  # Exclude 'id' for insertion
#     )
#     created_machinery = machinery_collection.find_one({"_id": new_machinery.inserted_id})
#     return convert_objectid_to_str(created_machinery)

# # POST Route to create new plant
# @router.post(
#     "/plant",
#     response_description="Add new plant",
#     response_model=Plant,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_plant(plant: Plant = Body(...)):
#     new_plant = plant_collection.insert_one(
#         plant.dict(exclude={"id"})  # Exclude 'id' for insertion
#     )
#     created_plant = plant_collection.find_one({"_id": new_plant.inserted_id})
#     return convert_objectid_to_str(created_plant)

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
