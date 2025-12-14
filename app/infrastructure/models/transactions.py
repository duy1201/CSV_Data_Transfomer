from sqlalchemy import Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from app.domain.entities import Transaction
from app.infrastructure.models.base_model import Base


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transaction_id_csv: Mapped[str] = mapped_column(String, index=True)

    file_id: Mapped[str] = mapped_column(ForeignKey("files.file_id"), index=True)

    date: Mapped[date] = mapped_column(Date)
    category: Mapped[str] = mapped_column(String, index=True)
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(3))

    # Relationship ngược lại
    file: Mapped["FileModel"] = relationship(back_populates="transactions")

    def to_entity(self) -> Transaction:
        return Transaction(
            transaction_id=self.transaction_id_csv,
            date=self.date,
            category=self.category,
            amount=self.amount,
            currency=self.currency
        )

    @staticmethod
    def from_entity(entity: Transaction, file_id: str) -> "TransactionModel":
        return TransactionModel(
            transaction_id_csv=entity.transaction_id,
            file_id=file_id,
            date=entity.date,
            category=entity.category,
            amount=entity.amount,
            currency=entity.currency
        )