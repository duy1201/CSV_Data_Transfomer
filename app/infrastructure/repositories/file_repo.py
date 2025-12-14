from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date

from sqlalchemy.orm import Session

from ..models.files import FileModel
from ...domain.entities import FileMetadata, Transaction, SummaryStats
from ..models.transactions import TransactionModel
from ...domain.interfaces import IFileRepository


class FileRepository(IFileRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, file_meta: FileMetadata) -> FileMetadata:
        db_model = FileModel.from_entity(file_meta)
        self.session.add(db_model)
        self.session.flush()
        return db_model.to_entity()

    def create_file_with_transactions(
            self,
            file_meta: FileMetadata,
            transactions: List[Transaction]
    ) -> None:
        db_file = FileModel.from_entity(file_meta)
        self.session.add(db_file)

        db_transactions = [
            TransactionModel.from_entity(t, file_id=file_meta.file_id)
            for t in transactions
        ]
        self.session.add_all(db_transactions)

        self.session.commit()

    def get_by_id(self, file_id: str) -> Optional[FileMetadata]:
        res = select(FileModel).where(FileModel.file_id == file_id)
        result = self.session.execute(res)

        db_model = result.scalar_one_or_none()
        return db_model.to_entity() if db_model else None

    def list_all(self) -> List[FileMetadata]:
        res = select(FileModel).order_by(FileModel.upload_time.desc())
        result = self.session.execute(res)

        return [f.to_entity() for f in result.scalars().all()]

    def get_transactions_by_file(
            self,
            file_id: str,
            page: int,
            page_size: int,
            category: Optional[str] = None,
            date_from: Optional[date] = None,
            date_to: Optional[date] = None
    ) -> List[Transaction]:

        res = select(TransactionModel).where(TransactionModel.file_id == file_id)

        if category:
            res = res.where(TransactionModel.category == category)
        if date_from:
            res = res.where(TransactionModel.date >= date_from)
        if date_to:
            res = res.where(TransactionModel.date <= date_to)

        offset = (page - 1) * page_size
        res = res.offset(offset).limit(page_size)

        result = self.session.execute(res)
        return [t.to_entity() for t in result.scalars().all()]

    def get_summary(self, file_id: str) -> SummaryStats:
        res_main = select(
            func.count(TransactionModel.id).label("count"),
            func.sum(TransactionModel.amount).label("total"),
            func.min(TransactionModel.date).label("min_date"),
            func.max(TransactionModel.date).label("max_date"),
            func.max(TransactionModel.currency).label("currency")
        ).where(TransactionModel.file_id == file_id)

        result_main = self.session.execute(res_main)
        row = result_main.one()

        res_cat = select(
            TransactionModel.category,
            func.count(TransactionModel.id),
            func.sum(TransactionModel.amount)
        ).where(
            TransactionModel.file_id == file_id
        ).group_by(TransactionModel.category)

        result_cat = self.session.execute(res_cat)

        category_stats = []
        for cat_name, cat_count, cat_total in result_cat:
            category_stats.append({
                "category": cat_name,
                "count": cat_count,
                "total": cat_total
            })

        return SummaryStats(
            total_transactions=row.count or 0,
            total_amount=row.total or 0.0,
            min_date=row.min_date,
            max_date=row.max_date,
            currency=row.currency or "USD",
            category_stats=category_stats
        )
