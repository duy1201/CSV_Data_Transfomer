import os
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Settings(BaseSettings):
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'CSV_Data_Transfomer')
    SECRET_KEY = os.getenv('SECRET_KEY', 'cdt_secret')
    API_PREFIX = ''
    BACKEND_CORS_ORIGINS = ['*']
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 # Token expired after 7 days
    SECURITY_ALGORITHM = 'HS256'
    LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'logging.ini')

    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')
    ADMIN_ID = os.getenv('ADMIN_ID', 1)

    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', 5432)
    DB_NAME = os.getenv('DB_NAME', 'csv_data_transformer')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')


settings = Settings()