# app/models/transaction.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from app.models.base import MongoBaseModel, PyObjectId

class TransactionCreate(BaseModel):
    user_id: str = "brother_dubai" # Hardcoded for MVP, dynamic later
    type: str = Field(..., pattern="^(income|expense)$")
    amount: float = Field(..., gt=0)
    currency: str = Field(..., pattern="^(AED|INR)$")
    category: str
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = None
    tags: List[str] = []
    
    # Cross-border logic: Always store the converted value based on the day's rate
    fx_rate_at_time: Optional[float] = None
    inr_equivalent: Optional[float] = None
    
    # AI Integration
    ai_generated: bool = False
    raw_ai_prompt: Optional[str] = None

class TransactionResponse(TransactionCreate, MongoBaseModel):
    pass