from fastapi import APIRouter, HTTPException, status
from basemodel import ItemInput, ItemOutput

router = APIRouter()

@router.post(
    "/user",
    response_description="Add new user",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_student(user: User = Body(...)):

    new_user = await user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user

