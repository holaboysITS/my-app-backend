from db import user_collection, plant_collection, machinery_collection

def test_connection():
    user = user_collection.find_one({})
    print(user)

test_connection()

#THIS IS JUST A TEST TO SEE IF YOU CAN CONNECT TO THE SERVER, YOU STILL NEED TO GET AN AUTH URI FROM MONGODB CLUSTER