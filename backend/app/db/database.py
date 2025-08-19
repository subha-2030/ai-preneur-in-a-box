import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from beanie import init_beanie
from app.models.user import User
from app.models.group import Group
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

client = AsyncIOMotorClient(DATABASE_URL)
db = client.get_database(os.getenv("MONGO_DATABASE"))

Base = declarative_base()

async def connect_to_mongo():
    try:
        await init_beanie(database=db, document_models=[User, Group])
        print("Successfully connected to MongoDB Atlas and initialized Beanie!")
    except Exception as e:
        print(f"Error connecting to MongoDB Atlas: {e}")

async def close_mongo_connection():
    client.close()
    print("MongoDB connection closed.")