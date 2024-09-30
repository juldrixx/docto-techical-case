"""
Main module for the FastAPI application.
"""
import os
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from database import crud, models, schemas as todoSchemas
from database.database import SessionLocal, engine
from s3 import actions, schemas as s3Schemas
from botocore.exceptions import ClientError
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
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


if not IS_TESTING:  # pragma: no cover
    models.Base.metadata.create_all(bind=engine)


def get_db():  # pragma: no cover
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


@app.get("/todos", response_model=todoSchemas.TodosResponse)
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
        todoSchemas.TodosResponse: The total count and the list of todos.
    """
    total_count, todos = crud.get_todos(db=db, skip=skip, limit=limit)
    return {"total": total_count, "todos": todos}


@app.post("/todos", response_model=todoSchemas.Todo)
def post_todo(todo: todoSchemas.TodoCreate, db: Session = Depends(get_db)):
    """Creates a new todo item.

    Accepts a `TodoCreate` schema as input, validates it, and persists the
    new todo to the database. The created todo is returned.

    Args:
        todo (todoSchemas.TodoCreate): The todo data to create, validated via
                                   Pydantic schema.
        db (Session, optional): The database session injected via `Depends(get_db)`.

    Returns:
        todoSchemas.Todo: The newly created todo item.
    """
    return crud.create_todo(db=db, todo=todo)


@app.delete("/todos/{todo_id}", response_model=todoSchemas.Todo)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Deletes a specific todo item by ID.

    Deletes the todo item corresponding to the provided `todo_id` from
    the database. If no todo is found with the given ID, a 404 HTTP
    exception is raised.

    Args:
        todo_id (int): The unique identifier of the todo item to delete.
        db (Session, optional): The database session injected via `Depends(get_db)`.

    Returns:
        todoSchemas.Todo: The deleted todo item.

    Raises:
        HTTPException: If no todo item with the specified ID is found,
                       raises a 404 Not Found error.
    """
    try:
        return crud.delete_todo(db=db, todo_id=todo_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="Todo not found") from e


@app.post("/objects")
async def post_object(file: UploadFile = File(...)):
    """
    Upload a file to the S3 bucket.

    **Args**:
    - file: The file to be uploaded (received as multipart/form-data).

    **Returns**:
    - JSON with a success message confirming the file was uploaded.

    **Raises**:
    - HTTPException: If there is an issue if the upload fails or reading the file.
    """
    try:
        file_content = await file.read()
        path = actions.put_object(name=file.filename, content=file_content)
        return {"message": f"File '{file.filename}' uploaded successfully to S3 bucket ({path})."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to upload file to S3: {str(e)}") from e


@app.get("/objects", response_model=s3Schemas.ListFilesResponse)
def get_objects():
    """
    List all files (names and paths) in the S3 bucket.

    **Returns**:
    - JSON object containing a list of files with their names and S3 paths.

    **Raises**:
    - HTTPException: If there is an issue with listing the files in the bucket.
    """
    try:
        return {"files": actions.list_objects()}
    except ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Error listing files: {str(e)}") from e


@app.delete("/objects/{file_name}", response_model=s3Schemas.DeleteResponse)
def delet_object(file_name: str):
    """
    Delete a file from the S3 bucket.

    **Args**:
    - file_name: The name of the file (S3 object key) to be deleted.

    **Returns**:
    - JSON with a success message confirming the file was deleted.

    **Raises**:
    - HTTPException: If there is an issue deleting the file.
    """
    try:
        path = actions.delete_object(name=file_name)
        return {"message": f"File '{file_name}' deleted successfully from S3 bucket ({path})."}
    except ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting files: {str(e)}") from e
