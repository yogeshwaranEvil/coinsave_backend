# app/models/remittance.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from app.models.base import MongoBaseModel

class RemittanceCreate(BaseModel):
    user_id: str = "brother_dubai"
    aed_sent: float = Field(..., gt=0, description="Amount deducted from Dubai bank")
    transfer_fee_aed: float = Field(default=0.0)
    exchange_rate_secured: float = Field(..., gt=0)
    inr_received: float = Field(..., gt=0, description="Amount credited to India bank")
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    destination_account: str = Field(..., description="e.g., HDFC Savings")
    notes: Optional[str] = None

class RemittanceResponse(RemittanceCreate, MongoBaseModel):
    pass