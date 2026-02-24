# app/core/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    """Establish connection to MongoDB."""
    db_instance.client = AsyncIOMotorClient(settings.MONGO_URI)
    db_instance.db = db_instance.client[settings.DATABASE_NAME]
    print(f"🟢 Connected to MongoDB: {settings.DATABASE_NAME}")

async def close_mongo_connection():
    """Close connection gracefully."""
    if db_instance.client is not None:
        db_instance.client.close()
        print("🔴 Closed MongoDB connection.")
        
def get_db():
    """Dependency injection helper for FastAPI routes."""
    return db_instance.db