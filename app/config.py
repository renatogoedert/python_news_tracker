import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://admin_username:admin_password@localhost:5432/news_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
