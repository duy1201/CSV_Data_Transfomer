import os, shutil, uuid
from datetime import datetime
from fastapi import UploadFile

from app.domain.entities import FileMetadata
from app.domain.interfaces import IFileRepository, IDataProcessor


class FileService:
    def __init__(self, repo: IFileRepository, processor: IDataProcessor, upload_dir: str):
        self.repo = repo
        self.processor = processor
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    def upload_file(self, file: UploadFile) -> FileMetadata:
        if not file.filename.endswith('.csv'):
            raise ValueError("Only CSV allowed")

        file_id = str(uuid.uuid4())
        save_path = os.path.join(self.upload_dir, f"{file.filename}")

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            transactions = self.processor.parse_transactions_from_file(save_path)
            meta = FileMetadata(file_id, file.filename, os.path.getsize(save_path), datetime.now(), save_path)
            self.repo.create_file_with_transactions(meta, transactions)
            return meta
        except Exception as e:
            if os.path.exists(save_path):
                os.remove(save_path)
            raise ValueError(f"Processing failed: {str(e)}")

    def get_all_files(self):
        return self.repo.list_all()

    def get_transactions(self, file_id, page, page_size, category, date_from, date_to):
        if not self.repo.get_by_id(file_id):
            raise ValueError("File not found")
        return self.repo.get_transactions_by_file(file_id, page, page_size, category, date_from, date_to)

    def get_file_summary(self, file_id):
        if not self.repo.get_by_id(file_id):
            raise ValueError("File not found")
        stats = self.repo.get_summary(file_id)
        return {
            "file_id": file_id, "total_transactions": stats.total_transactions,
            "total_amount": stats.total_amount, "currency": stats.currency,
            "date_range": {"start": stats.min_date, "end": stats.max_date},
            "by_category": stats.category_stats
        }
