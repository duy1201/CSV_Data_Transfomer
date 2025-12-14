from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from .entities import FileMetadata, Transaction, SummaryStats


class IFileRepository(ABC):
    @abstractmethod
    def save(self, file_meta: FileMetadata) -> FileMetadata: ...

    @abstractmethod
    def create_file_with_transactions(self, file_meta: FileMetadata, transactions: List[Transaction]) -> None: ...

    @abstractmethod
    def get_by_id(self, file_id: str) -> Optional[FileMetadata]: ...

    @abstractmethod
    def list_all(self) -> List[FileMetadata]: ...

    @abstractmethod
    def get_transactions_by_file(
            self,
            file_id: str,
            page: int,
            page_size: int,
            category: Optional[str] = None,
            date_from: Optional[date] = None,
            date_to: Optional[date] = None
    ) -> List[Transaction]: ...

    @abstractmethod
    def get_summary(self, file_id: str) -> SummaryStats: ...


class IDataProcessor(ABC):
    @abstractmethod
    def parse_transactions_from_file(self, file_path: str) -> List[Transaction]: ...