# app/api/routes_transactions.py
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List

from app.core.database import get_db
from app.models.transaction import TransactionCreate, TransactionResponse

router = APIRouter()

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate, 
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Convert Pydantic model to dictionary
    transaction_dict = transaction.model_dump(by_alias=True, exclude_none=True)
    
    # Insert into MongoDB
    new_transaction = await db["transactions"].insert_one(transaction_dict)
    
    # Fetch the created document to return it
    created_transaction = await db["transactions"].find_one({"_id": new_transaction.inserted_id})
    return created_transaction

@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    currency: str = None, 
    type: str = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Build a dynamic query based on optional filters
    query = {}
    if currency:
        query["currency"] = currency.upper()
    if type:
        query["type"] = type.lower()
        
    transactions_cursor = db["transactions"].find(query).sort("date", -1) # Newest first
    transactions = await transactions_cursor.to_list(length=100) # Limit for MVP
    return transactions

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    id: str, 
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    delete_result = await db["transactions"].delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")