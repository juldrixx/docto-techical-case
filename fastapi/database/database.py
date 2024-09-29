"""
This module establishes a connection to a MySQL database using SQLAlchemy.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB")
DB_URL = f"mysql+pymysql://{MYSQL_USER}:{
    MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(url=DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy declarative models.

    This class serves as a base for all ORM models in the application.
    It inherits from SQLAlchemy's DeclarativeBase, allowing for the 
    creation of model classes that are mapped to database tables.

    Args:
        DeclarativeBase (type): The base class for declarative class definitions
        from SQLAlchemy, providing the necessary functionality for 
        mapping Python classes to database tables.
    """
