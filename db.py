import os
from dotenv import load_dotenv
from pymongo.collection import Collection
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI_OFF"))
db = client.get_database("project_group3")
user_collection = db.get_collection("users")
plant_collection = db.get_collection("plants")
machinery_collection = db.get_collection("machinery")