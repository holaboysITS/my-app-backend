# my-app-backend
backend for my-app project cringe

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