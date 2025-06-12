#configuration settings, could have diferent confs for dev, test, and prod
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://admin_username:admin_password@db:5432/news_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
