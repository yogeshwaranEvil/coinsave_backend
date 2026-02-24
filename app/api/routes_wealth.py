# app/api/routes_wealth.py
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List

from app.core.database import get_db
from app.models.wealth import WealthItemCreate, WealthItemResponse

router = APIRouter()

@router.post("/", response_model=WealthItemResponse, status_code=status.HTTP_201_CREATED)
async def create_wealth_item(
    item: WealthItemCreate, 
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    item_dict = item.model_dump(by_alias=True, exclude_none=True)
    new_item = await db["wealth"].insert_one(item_dict)
    created_item = await db["wealth"].find_one({"_id": new_item.inserted_id})
    return created_item

@router.get("/", response_model=List[WealthItemResponse])
async def get_wealth_items(
    class_type: str = None, # 'asset' or 'liability'
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    query = {}
    if class_type:
        query["class_type"] = class_type.lower()
        
    items_cursor = db["wealth"].find(query)
    items = await items_cursor.to_list(length=100)
    return items