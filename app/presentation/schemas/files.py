from typing import List

from pydantic import BaseModel
from datetime import datetime, date


class FileMetadataResponse(BaseModel):
    file_id: str
    filename: str
    size: int
    upload_time: datetime
    class Config: from_attributes = True

class TransactionResponse(BaseModel):
    transaction_id: str
    date: date
    category: str
    amount: float
    currency: str

class SummaryResponse(BaseModel):
    file_id: str
    total_transactions: int
    total_amount: float
    currency: str
    date_range: dict
    by_category: List[dict]