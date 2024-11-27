import asyncio
from db import user_collection

async def test_connection():
    user = await user_collection.find_one({})
    print(user)

asyncio.run(test_connection())

#THIS IS JUST A TEST TO SEE IF YOU CAN CONNECT TO THE SERVER, YOU STILL NEED TO GET AN AUTH URI FROM MONGODB CLUSTER