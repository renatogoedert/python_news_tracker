#configuration settings, could have diferent confs for dev, test, and prod
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_USERNAME = os.getenv("POSTGRES_USER", "admin_username")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin_password")
    DB_NAME     = os.getenv("POSTGRES_DB", "news_db")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}"
        f"@db:5432/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
