# app/api/routes_remittance.py
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List

from app.core.database import get_db
# (Assuming you saved the remittance model from the previous step as RemittanceCreate/Response in app/models/remittance.py)
from app.models.remittance import RemittanceCreate, RemittanceResponse

router = APIRouter()

@router.post("/", response_model=RemittanceResponse, status_code=status.HTTP_201_CREATED)
async def create_remittance(
    remittance: RemittanceCreate, 
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    remittance_dict = remittance.model_dump(by_alias=True, exclude_none=True)
    new_remittance = await db["remittances"].insert_one(remittance_dict)
    created_remittance = await db["remittances"].find_one({"_id": new_remittance.inserted_id})
    return created_remittance

@router.get("/", response_model=List[RemittanceResponse])
async def get_remittances(
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    remittances_cursor = db["remittances"].find().sort("date", -1)
    remittances = await remittances_cursor.to_list(length=100)
    return remittances