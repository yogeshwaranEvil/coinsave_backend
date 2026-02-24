# app/models/rates.py
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from app.models.base import MongoBaseModel

class MarketRatesUpdate(BaseModel):
    aed_to_inr: float
    gold_24k_inr_per_gram: float
    silver_inr_per_gram: float
    last_fetched: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MarketRatesResponse(MarketRatesUpdate, MongoBaseModel):
    pass