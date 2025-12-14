import pytest
from unittest.mock import MagicMock
from datetime import date, datetime

from fastapi import UploadFile

from app.application.services.file_srv import FileService
from app.domain.entities import FileMetadata, Transaction, SummaryStats


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def mock_processor():
    return MagicMock()


@pytest.fixture
def file_service(mock_repo, mock_processor):
    return FileService(repo=mock_repo, processor=mock_processor, upload_dir="/tmp")


def test_upload_file_wrong_extension(file_service):
    file = MagicMock(spec=UploadFile)
    file.filename = "image.png"

    with pytest.raises(ValueError) as excinfo:
        file_service.upload_file(file)

    assert "Only CSV allowed" in str(excinfo.value)


def test_upload_file_success(file_service, mock_repo, mock_processor):
    file = MagicMock(spec=UploadFile)
    file.filename = "data.csv"
    file.file = MagicMock()
    file.file.read.side_effect = [b"transaction_id,amount\n1,100", b""]

    mock_processor.parse_transactions_from_file.return_value = []

    result = file_service.upload_file(file)

    assert result.filename == "data.csv"
    mock_repo.create_file_with_transactions.assert_called_once()
    mock_processor.parse_transactions_from_file.assert_called_once()


def test_get_all_files(file_service, mock_repo):
    mock_files = [
        FileMetadata(file_id="1", filename="a.csv", size=100, upload_time=datetime.now(), path="p1"),
        FileMetadata(file_id="2", filename="b.csv", size=200, upload_time=datetime.now(), path="p2")
    ]
    mock_repo.list_all.return_value = mock_files

    result = file_service.get_all_files()

    assert len(result) == 2
    assert result[0].filename == "a.csv"
    mock_repo.list_all.assert_called_once()


def test_get_transactions_success(file_service, mock_repo):
    file_id = "existing_id"
    mock_repo.get_by_id.return_value = FileMetadata("existing_id", "a.csv", 100, datetime.now(), "p")
    mock_trans = [Transaction("tx1", date.today(), "Food", 10.0, "USD")]
    mock_repo.get_transactions_by_file.return_value = mock_trans

    result = file_service.get_transactions(file_id, page=1, page_size=10, category=None, date_from=None, date_to=None)

    assert len(result) == 1
    assert result[0].transaction_id == "tx1"
    mock_repo.get_transactions_by_file.assert_called_with(
        file_id, 1, 10, None, None, None
    )


def test_get_transactions_file_not_found(file_service, mock_repo):
    file_id = "non_existent_id"
    mock_repo.get_by_id.return_value = None

    with pytest.raises(ValueError) as excinfo:
        file_service.get_transactions(file_id, 1, 10, None, None, None)

    assert f"File not found" in str(excinfo.value)
    mock_repo.get_transactions_by_file.assert_not_called()


def test_get_summary_success(file_service, mock_repo):
    file_id = "f1"
    mock_repo.get_by_id.return_value = MagicMock()

    expected_stats = SummaryStats(
        total_transactions=5,
        total_amount=500.0,
        min_date=date.today(),
        max_date=date.today(),
        currency="USD",
        category_stats=[]
    )
    mock_repo.get_summary.return_value = expected_stats

    result = file_service.get_file_summary(file_id)

    assert result["total_transactions"] == 5
    assert result["total_amount"] == 500.0
    mock_repo.get_summary.assert_called_once_with(file_id)


def test_get_summary_file_not_found(file_service, mock_repo):
    mock_repo.get_by_id.return_value = None

    with pytest.raises(ValueError):
        file_service.get_file_summary("missing_id")