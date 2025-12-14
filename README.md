# API Xử Lý Dữ Liệu Giao Dịch CSV (CSV Data Transformer API)

Dự án này là một dịch vụ RESTful API hiệu năng cao được xây dựng bằng **FastAPI**, có chức năng xử lý các tệp tin giao dịch (CSV), lưu trữ vào **PostgreSQL**

Hệ thống được thiết kế tuân thủ nghiêm ngặt theo **Clean Architecture** để đảm bảo khả năng mở rộng (scalability), dễ bảo trì (maintainability) và dễ kiểm thử (testability).

---

## 🏗 Tổng Quan Kiến Trúc (Architecture Overview)

Dự án áp dụng mô hình **Clean Architecture** (hay còn gọi là Hexagonal Architecture / Cosmic Python), phân tách ứng dụng thành các tầng (layers) riêng biệt với trách nhiệm rõ ràng.

### 1. Cấu Trúc Thư Mục & Trách Nhiệm

```text
app/
├── domain/                 # Lớp Nghiệp Vụ Cốt Lõi (Business Logic)
│   ├── entities/           # Các thực thể dữ liệu thuần túy (FileMetadata, Transaction)
│   └── interfaces/         # Các giao diện trừu tượng (Abstract Classes)
│
├── application/            # Lớp Ứng Dụng (Application Logic)
│   └── services/           # Điều phối luồng dữ liệu, chứa các Use Cases (FileService)
│
├── infrastructure/         # Lớp Cơ Sở Hạ Tầng (Adapters/External)
│   ├── core 
│   │    ├── config.py       # Thiết lập biến cài đặt
│   │    ├── dependencies.py # Các hàm dependency 
│   │    └── security.py     # Logic xác thực JWT
│   ├── database/           # Kết nối Database & Quản lý Session
│   ├── models/             # Các bảng CSDL (SQLAlchemy Models)
│   ├── repositories/       # Triển khai cụ thể các Interface của Domain
│   └── data_processor.py   # Logic xử lý CSV (Sử dụng thư viện Pandas)
└── presentation/           # Lớp Giao Diện (Entry Points)
    ├── api/                # FastAPI Routers & Dependencies
    └── schemas/            # Pydantic Schemas (DTOs) cho Request/Response
```

### 2. Luồng Dữ Liệu (Data Flow)
Dữ liệu di chuyển một chiều từ các lớp bên ngoài vào trong thông qua cơ chế Dependency Injection (DI):

Request → Router (Presentation) → Service (Application) → Repository (Infrastructure) → Database

Ví dụ: Luồng Upload File

Router: Nhận POST /upload, kiểm tra JWT Token.

Service: Nhận UploadFile, lưu file vật lý xuống đĩa, gọi DataProcessor để đọc CSV.

Repository: Nhận các Entities từ Service, chuyển đổi sang DB Models, và thực hiện Bulk Insert (chèn hàng loạt).

Database: Lưu dữ liệu vào bảng files và transactions.

### 3. Các Mẫu Thiết Kế (Design Patterns)
Repository Pattern: Tách biệt logic nghiệp vụ khỏi logic truy xuất dữ liệu. Service chỉ giao tiếp với IFileRepository (trừu tượng), cho phép dễ dàng thay đổi DB (ví dụ: chuyển sang MockDB khi test) mà không sửa code nghiệp vụ.

Dependency Injection (DI): Sử dụng Depends của FastAPI để "tiêm" (inject) Database Session và Repository vào Service. Giúp code lỏng lẻo (loose coupling) và dễ viết Unit Test.

## Installation

- Clone Project
- Cài đặt Postgresql & Create Database
- Cài đặt requirements.txt
- Run project ở cổng 8000
```
// Clone project & run
$ virtualenv -p python3 .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ cp env.example .env       // Recheck SQL_DATABASE_URL ở bước này
$ alembic upgrade head
$ uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
