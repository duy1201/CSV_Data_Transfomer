from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, List

@dataclass
class FileMetadata:
    file_id: str
    filename: str
    size: int
    upload_time: datetime
    path: str

@dataclass
class Transaction:
    transaction_id: str
    date: date
    category: str
    amount: float
    currency: str

@dataclass
class SummaryStats:
    total_transactions: int
    total_amount: float
    min_date: Optional[date]
    max_date: Optional[date]
    currency: str
    category_stats: List[dict]