import os
from dotenv import load_dotenv
from pymongo.collection import Collection
import motor.motor_asyncio

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL")) #env variable
db = client.get_database("project_group3")
user_collection = db.get_collection("users")
plant_collection = db.get_collection("plants")
machinery_collection = db.get_collection("machineries")