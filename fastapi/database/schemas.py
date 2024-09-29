"""
This module defines Pydantic models used for validating and serializing 
data in a Todo application.
"""
from typing import List
from pydantic import BaseModel


class TodoBase(BaseModel):
    """Base model for a todo item.

    This class defines the core fields that are common for both 
    input and output operations related to a todo item.

    Attributes:
        label (str): The description or title of the todo item.
        quantity (int): The number of items or tasks associated with 
                        the todo.
    """
    label: str
    quantity: int


class TodoCreate(TodoBase):
    """Model for creating a new todo item.

    Inherits all attributes from TodoBase. This class is typically used 
    when validating input data for creating a new todo item.
    """


class Todo(TodoBase):
    """Model representing a todo item with an ID.

    This model is used for returning todo items from the database, 
    including the `id` field.

    Attributes:
        id (int): The unique identifier for the todo item.

    Config:
        orm_mode (bool): Enables interaction with ORM objects, allowing 
                         this model to map data directly from database 
                         entities like SQLAlchemy models.
    """
    id: int

    class Config:
        """Pydantic configuration settings for the Todo model.

        Attributes:
            orm_mode (bool): If set to True, allows Pydantic to read 
                             data from ORM objects (e.g., SQLAlchemy models), 
                             converting them into Pydantic models seamlessly. 
                             This is particularly useful when returning 
                             database objects via API responses without 
                             manually converting them to dictionaries.
        """
        orm_mode = True


class TodosResponse(BaseModel):
    """Model representing a response containing multiple todo items.

    This model is used for paginated or list-based responses that return 
    a collection of todo items, along with the total number of todos.

    Attributes:
        total (int): The total number of todo items in the collection.
        todos (List[Todo]): A list of `Todo` objects representing each 
                            todo item.
    """
    total: int
    todos: List[Todo]
