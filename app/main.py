# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.routes_transactions import router as transactions_router
from app.api.routes_wealth import router as wealth_router
from app.api.routes_remittance import router as remittance_router


# Lifespan context manager replaces the old @app.on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    # What happens when server starts
    await connect_to_mongo()
    yield
    # What happens when server shuts down
    await close_mongo_connection()

app = FastAPI(
    title="Cross-Border Wealth API",
    description="Backend for AED/INR Expense and Net Worth Tracker",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Setup - Essential for connecting to the React Vite frontend later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {
        "status": "online", 
        "message": "Cross-Border Wealth API is running. Systems nominal."
    }


# Update app/main.py to include the following lines below your existing code:

# Include the routers with prefixes
app.include_router(transactions_router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(wealth_router, prefix="/api/wealth", tags=["Wealth & Assets"])
app.include_router(remittance_router, prefix="/api/remittances", tags=["Cross-Border Remittances"])