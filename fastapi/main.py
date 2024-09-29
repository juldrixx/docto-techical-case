"""
Main module for the FastAPI application.
"""
import os
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from database import crud, models, schemas
from database.database import SessionLocal, engine
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

IS_TESTING = os.getenv('TESTING', 'false').lower() == 'true'
FASTAPI_ROOT_PATH = os.getenv('FASTAPI_ROOT_PATH', "")


app = FastAPI(root_path=FASTAPI_ROOT_PATH)

origins = [
    "http://localhost",
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if not IS_TESTING: # pragma: no cover
    models.Base.metadata.create_all(bind=engine)


def get_db(): # pragma: no cover
    """Dependency function to provide a database session.

    This function is used as a dependency in FastAPI to inject 
    a SQLAlchemy session (`db`) into the request handlers. It ensures 
    that the database session is correctly opened and closed.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    """Root API endpoint.

    This is the default endpoint of the FastAPI application.

    Returns:
        str: A basic string response indicating the root of the API.
    """
    return "Hello, this message comes from the Fast API root endpoint!"


@app.get("/todos", response_model=schemas.TodosResponse)
def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Fetches a paginated list of todo items.

    Queries the database to retrieve todo items with optional pagination 
    using `skip` and `limit` query parameters. Returns the total number 
    of todos and a list of todo items.

    Args:
        skip (int, optional): The number of todo items to skip (default 0).
        limit (int, optional): The maximum number of todo items to return (default 100).
        db (Session, optional): The database session injected via `Depends(get_db)`.

    Returns:
        schemas.TodosResponse: The total count and the list of todos.
    """
    total_count, todos = crud.get_todos(db=db, skip=skip, limit=limit)
    return {"total": total_count, "todos": todos}


@app.post("/todos", response_model=schemas.Todo)
def post_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """Creates a new todo item.

    Accepts a `TodoCreate` schema as input, validates it, and persists the 
    new todo to the database. The created todo is returned.

    Args:
        todo (schemas.TodoCreate): The todo data to create, validated via 
                                   Pydantic schema.
        db (Session, optional): The database session injected via `Depends(get_db)`.

    Returns:
        schemas.Todo: The newly created todo item.
    """
    return crud.create_todo(db=db, todo=todo)


@app.delete("/todos/{todo_id}", response_model=schemas.Todo)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Deletes a specific todo item by ID.

    Deletes the todo item corresponding to the provided `todo_id` from 
    the database. If no todo is found with the given ID, a 404 HTTP 
    exception is raised.

    Args:
        todo_id (int): The unique identifier of the todo item to delete.
        db (Session, optional): The database session injected via `Depends(get_db)`.

    Returns:
        schemas.Todo: The deleted todo item.

    Raises:
        HTTPException: If no todo item with the specified ID is found, 
                       raises a 404 Not Found error.
    """
    try:
        return crud.delete_todo(db=db, todo_id=todo_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="Todo not found") from e
