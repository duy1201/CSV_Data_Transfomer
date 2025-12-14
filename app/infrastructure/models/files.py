from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from app.domain.entities import FileMetadata
from app.infrastructure.models.base_model import Base


class FileModel(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(String, index=True, unique=True)
    filename: Mapped[str] = mapped_column(String)
    size: Mapped[int] = mapped_column(Integer)
    upload_time: Mapped[datetime] = mapped_column(Date, default=datetime.now().date())
    path: Mapped[str] = mapped_column(String)

    transactions: Mapped[List["TransactionModel"]] = relationship(
        back_populates="file",
        cascade="all, delete-orphan"
    )

    def to_entity(self) -> FileMetadata:
        return FileMetadata(
            file_id=self.file_id,
            filename=self.filename,
            size=self.size,
            upload_time=self.upload_time,
            path=self.path
        )

    @staticmethod
    def from_entity(entity: FileMetadata) -> "FileModel":
        return FileModel(
            file_id=entity.file_id,
            filename=entity.filename,
            size=entity.size,
            upload_time=entity.upload_time,
            path=entity.path
        )

