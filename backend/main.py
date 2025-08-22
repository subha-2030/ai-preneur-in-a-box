from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.api.v1.api import api_router
from app.db.database import connect_to_mongo, close_mongo_connection

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost:3000",
    # Add other origins if needed, e.g., your production frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add SessionMiddleware
# Make sure to set a SECRET_KEY in your .env file
import os
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("SECRET_KEY"),
    same_site="lax"  # Allow cookies in cross-site navigation (OAuth redirects)
)


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


app.include_router(api_router, prefix="/api/v1")