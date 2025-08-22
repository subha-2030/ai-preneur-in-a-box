import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from beanie import init_beanie
from app.models.user import User
from app.models.meeting_note import MeetingNote
from app.models.client import Client
from app.models.briefing import ResearchBriefing
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Configure MongoDB client with SSL settings to handle certificate issues
client = AsyncIOMotorClient(
    DATABASE_URL,
    tls=True,
    tlsAllowInvalidCertificates=True,
    tlsAllowInvalidHostnames=True,
    serverSelectionTimeoutMS=5000
)
db = client.get_database(os.getenv("MONGO_DATABASE"))

Base = declarative_base()

async def connect_to_mongo():
    try:
        await init_beanie(database=db, document_models=[User, MeetingNote, Client, ResearchBriefing])
        print("Successfully connected to MongoDB Atlas and initialized Beanie!")
    except Exception as e:
        print(f"Error connecting to MongoDB Atlas: {e}")

async def close_mongo_connection():
    client.close()
    print("MongoDB connection closed.")