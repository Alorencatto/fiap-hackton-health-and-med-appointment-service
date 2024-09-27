import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    INVENTORY_SERVICE_BASE_URL = os.getenv("APPOINTMENT_SERVICE_BASE_URL")
    BROKER_HOST = os.getenv("BROKER_HOST")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
