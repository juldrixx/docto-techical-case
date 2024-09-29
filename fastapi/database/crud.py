"""
This module contains the database operations for interacting with 
todo items in the application.
"""
from sqlalchemy.orm import Session

from . import models, schemas


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    """Fetches a list of todo items from the database.

    Queries the database to retrieve todo items with optional 
    pagination controls for skipping and limiting the number 
    of results.

    Args:
        db (Session): The SQLAlchemy database session used for querying.
        skip (int, optional): The number of todo items to skip in the result set. 
                              Defaults to 0.
        limit (int, optional): The maximum number of todo items to return. 
                               Defaults to 100.

    Returns:
        tuple: A tuple containing:
            - total_count (int): The total number of todo items in the database.
            - todos (List[models.Todo]): A list of todo items from the database 
                                         based on the applied pagination.
    """
    todos = db.query(models.Todo).offset(skip).limit(limit).all()
    total_count = db.query(models.Todo).count()
    return total_count, todos


def create_todo(db: Session, todo: schemas.TodoCreate):
    """Creates a new todo item in the database.

    Uses the provided schema to create a new todo record in the 
    database, commits the transaction, and refreshes the session 
    to return the newly created todo item.

    Args:
        db (Session): The SQLAlchemy database session used for the transaction.
        todo (schemas.TodoCreate): The data required to create a new todo item, 
                                   validated through the Pydantic schema.

    Returns:
        models.Todo: The newly created todo item after being persisted 
                     to the database.
    """
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    """Deletes a specific todo item from the database.

    Queries the database for a todo item by its ID, deletes the item 
    from the database, and commits the transaction.

    Args:
        db (Session): The SQLAlchemy database session used for the transaction.
        todo_id (int): The unique identifier of the todo item to be deleted.

    Returns:
        models.Todo: The deleted todo item.
        
    Raises:
        NoResultFound: If no todo item with the specified ID exists.
    """
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).one()
    db.delete(db_todo)
    db.commit()
    return db_todo
