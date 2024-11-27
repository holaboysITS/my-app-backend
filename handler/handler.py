from fastapi import APIRouter, HTTPException, status
from basemodel import User, Plant, Machinery
from db import user_collection, machinery_collection, plant_collection

router = APIRouter()

@router.post(
    "/user",
    response_description="Add new user",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
def create_student(user: User):

    new_user = user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user

