# app/models/wealth.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from app.models.base import MongoBaseModel

class WealthItemCreate(BaseModel):
    user_id: str = "brother_dubai"
    class_type: str = Field(..., pattern="^(asset|liability)$")
    category: str = Field(..., description="bank, gold, silver, personal_loan, gold_loan")
    name: str = Field(..., description="e.g., '24k Physical Gold' or 'HDFC Personal Loan'")
    
    # Value can be monetary OR weight
    balance_or_quantity: float
    unit: str = Field(..., pattern="^(AED|INR|grams)$")
    
    # For Liabilities
    interest_rate: Optional[float] = None
    emi_amount: Optional[float] = None
    
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class WealthItemResponse(WealthItemCreate, MongoBaseModel):
    pass