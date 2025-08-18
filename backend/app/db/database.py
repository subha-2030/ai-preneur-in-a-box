import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

client = AsyncIOMotorClient(DATABASE_URL)
db = client.get_database(os.getenv("MONGO_DATABASE"))

async def connect_to_mongo():
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print(f"Error connecting to MongoDB Atlas: {e}")

async def close_mongo_connection():
    client.close()
    print("MongoDB connection closed.")