# pylint: disable=redefined-outer-name
"""
Test module for FastAPI endpoints related to Todo items.
"""
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
import pytest
from main import app, get_db
from botocore.exceptions import ClientError
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture
def db_session_mock():
    """
    Fixture to create a mock database session.

    This fixture returns a MagicMock instance that simulates
    the SQLAlchemy Session interface, allowing tests to run
    without an actual database connection.

    Yields:
        MagicMock: A mock object mimicking the Session class.
    """
    db_mock = MagicMock(spec=Session)
    yield db_mock


@pytest.fixture(autouse=True)
def override_get_db(db_session_mock):
    """
    Fixture to override the dependency for the database session.

    This fixture automatically replaces the `get_db` dependency in the
    FastAPI application with a mock session for all tests in this module,
    ensuring that tests do not require a real database.

    Args:
        db_session_mock (MagicMock): The mocked database session to use.
    """
    app.dependency_overrides[get_db] = lambda: db_session_mock


@pytest.fixture
def override_s3_utils():
    """
    Fixture to override S3 utility functions with mocks for testing.

    This fixture replaces the actual S3 functions with mocks to
    simulate S3 interactions, ensuring tests do not require real
    AWS credentials or a live S3 bucket.
    """
    with patch("s3.actions.put_object") as mock_put, \
            patch("s3.actions.list_objects") as mock_list, \
            patch("s3.actions.delete_object") as mock_delete, \
            patch("s3.actions.get_object") as mock_get:
        yield mock_put, mock_list, mock_delete, mock_get


def test_main_root():
    """
    Test the root endpoint of the FastAPI application.

    This test sends a GET request to the root endpoint ("/") and
    asserts that the response status code is 200 and that the
    returned JSON message is as expected.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello, this message comes from the Fast API root endpoint!"


def test_get_todos(db_session_mock):
    """
    Test the GET /todos endpoint.

    This test simulates retrieving todo items from the database. It mocks
    the database query and the CRUD function to return predefined todo items.
    It then asserts that the response status code is 200 and that the
    returned JSON matches the expected structure.

    Args:
        db_session_mock (MagicMock): The mocked database session.
    """
    mock_todos = [{"id": 1, "label": "Test Todo", "quantity": 1}]
    query = db_session_mock.query
    query.return_value.offset.return_value.limit.return_value.all.return_value = mock_todos
    query.return_value.count.return_value = 1

    with patch("database.crud.get_todos", return_value=(1, mock_todos)):
        response = client.get("/todos?skip=0&limit=10")

    assert response.status_code == 200
    assert response.json() == {
        "total": 1,
        "todos": mock_todos
    }


def test_post_todo_success():
    """
    Test the POST /todos endpoint for successful todo creation.

    This test sends a POST request with new todo data to the
    /todos endpoint. It mocks the create_todo function to return
    a predefined created todo item and asserts that the response
    status code is 200 and the returned JSON matches the expected
    created todo.
    """
    new_todo_data = {
        "label": "New Todo",
        "quantity": 1
    }
    created_todo = {
        "id": 1,
        "label": "New Todo",
        "quantity": 1
    }

    with patch("database.crud.create_todo", return_value=created_todo):
        response = client.post("/todos", json=new_todo_data)

    assert response.status_code == 200
    assert response.json() == created_todo


def test_delete_todo_success():
    """
    Test the DELETE /todos/{todo_id} endpoint for successful deletion.

    This test sends a DELETE request for a specific todo item. It
    mocks the delete_todo function to return the deleted todo item
    and asserts that the response status code is 200 and the returned
    JSON matches the deleted item.
    """
    todo_id = 1
    todo_item = {
        "id": todo_id,
        "label": "Test Todo",
        "quantity": 0
    }

    with patch("database.crud.delete_todo", return_value=todo_item):
        response = client.delete(f"/todos/{todo_id}")

    assert response.status_code == 200
    assert response.json() == todo_item


def test_delete_todo_not_found():
    """
    Test the DELETE /todos/{todo_id} endpoint when todo is not found.

    This test sends a DELETE request for a todo item that does not exist.
    It mocks the delete_todo function to raise a NoResultFound exception
    and asserts that the response status code is 404 and that the
    returned JSON indicates that the todo was not found.
    """
    todo_id = 999

    with patch("database.crud.delete_todo", side_effect=NoResultFound):
        response = client.delete(f"/todos/{todo_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_post_object_success(override_s3_utils):
    """
    Test the POST /objects endpoint for successful file upload.

    This test simulates uploading a file to S3 and asserts that
    the response contains the expected success message.
    """
    mock_put, _, _, _ = override_s3_utils
    mock_put.return_value = "s3://your-bucket/myfile.txt"

    file_data = b"Sample file content"
    response = client.post(
        "/objects", files={"file": ("myfile.txt", file_data)})

    assert response.status_code == 200
    assert response.json() == {
        "message":
        "File 'myfile.txt' uploaded successfully to S3 bucket (s3://your-bucket/myfile.txt)."
    }


def test_post_object_failure(override_s3_utils):
    """
    Test the POST /objects endpoint for failed file upload.

    This test simulates uploading a file to S3 and asserts that
    the response contains the expected error message.
    """
    mock_put, _, _, _ = override_s3_utils
    mock_put.side_effect = Exception("S3 upload error")

    # Create a dummy file-like object
    file_data = b"Sample file content"
    response = client.post(
        "/objects", files={"file": ("myfile.txt", file_data)})

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Failed to upload file to S3: S3 upload error"}


def test_get_objects_success(override_s3_utils):
    """
    Test the GET /objects endpoint for listing files in S3.

    This test simulates retrieving the list of files from S3 and
    asserts that the response matches the expected structure.
    """
    _, mock_list, _, _ = override_s3_utils
    mock_list.return_value = [
        {"name": "myfile.txt", "path": "s3://your-bucket/myfile.txt"},
        {"name": "anotherfile.txt", "path": "s3://your-bucket/anotherfile.txt"}
    ]

    response = client.get("/objects")

    assert response.status_code == 200
    assert response.json() == {"files": mock_list.return_value}


def test_get_objects_failure(override_s3_utils):
    """
    Test the GET /objects endpoint for failure in listing files from S3.

    This test simulates an error when attempting to retrieve the list of files from S3
    and asserts that the response matches the expected error structure.
    """
    _, mock_list, _, _ = override_s3_utils
    mock_list.side_effect = ClientError(
        {"Error": {"Code": "404", "Message": "Not Found"}},
        "ListObjects"
    )

    response = client.get("/objects")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Error listing files: An error occurred (404) when calling the ListObjects operation: Not Found"}


def test_delete_object_success(override_s3_utils):
    """
    Test the DELETE /object/{file_name} endpoint for successful file deletion.

    This test simulates deleting a file from S3 and asserts that
    the response contains the expected success message.
    """
    _, _, mock_delete, _ = override_s3_utils
    mock_delete.return_value = "s3://your-bucket/myfile.txt"

    response = client.delete("/objects/myfile.txt")

    assert response.status_code == 200
    assert response.json() == {
        "message":
        "File 'myfile.txt' deleted successfully from S3 bucket (s3://your-bucket/myfile.txt)."
    }


def test_delete_object_failure(override_s3_utils):
    """
    Test the DELETE /object/{file_name} endpoint for failure in file deletion.

    This test simulates an error when attempting to delete a file from S3
    and asserts that the response matches the expected error structure.
    """
    _, _, mock_delete, _ = override_s3_utils
    mock_delete.side_effect = ClientError(
        {"Error": {"Code": "404", "Message": "Not Found"}},
        "DeleteObject"
    )

    response = client.delete("/objects/myfile.txt")

    assert response.status_code == 500
    assert response.json() == {
        "detail":
        "Error deleting files: An error occurred (404) when calling the DeleteObject operation: Not Found"
    }


def test_get_object_success(override_s3_utils):
    """
    Test the GET /objects/{file_name} endpoint for successful file download.

    This test simulates downloading a file from S3 and verifies that the response
    contains the expected file content and correct headers.
    """
    file_name = "myfile.txt"
    file_content = b"Sample file content"

    _, _, _, mock_get = override_s3_utils
    mock_get.return_value = file_content

    response = client.get(f"/objects/{file_name}")

    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == f'attachment; filename={
        file_name}'
    assert response.content == file_content


def test_get_object_not_found(override_s3_utils):
    """
    Test the GET /objects/{file_name} endpoint when the file is not found.

    This test simulates a scenario where the requested file does not exist in S3
    and verifies that the appropriate HTTP exception is raised.
    """
    file_name = "non_existent_file.txt"

    _, _, _, mock_get = override_s3_utils
    mock_get.side_effect = ClientError(
        {"Error": {"Code": "404", "Message": "Not Found"}},
        "GetObject"
    )

    response = client.get(f"/objects/{file_name}")

    assert response.status_code == 500
    assert response.json() == {
        "detail":
        "Error downloading file: An error occurred (404) when calling the GetObject operation: Not Found"
    }
