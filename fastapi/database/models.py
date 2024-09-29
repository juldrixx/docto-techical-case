"""
This module defines the SQLAlchemy ORM models for the application.
"""
from sqlalchemy import Column, Integer, String
from .database import Base


class Todo(Base):
    """Represents a task in a to-do list.

    This class defines the structure of the 'todos' table in the 
    database, which is used to store information about individual 
    to-do items. Each item contains an identifier, a label, and 
    a quantity, allowing for basic task management.

    Attributes:
        id (int): The primary key of the to-do item. This is 
                  automatically generated and unique for each item.
        label (str): A brief description or title of the to-do item, 
                     with a maximum length of 255 characters. This field 
                     is indexed to facilitate quick searches.
        quantity (int): An integer representing the number of tasks or 
                        items associated with this to-do. This field is 
                        also indexed for efficient querying.

    Usage:
        Instances of the Todo class can be created, modified, 
        and persisted to the database using SQLAlchemy session objects.
    """
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(255), index=True)
    quantity = Column(Integer, index=True)
