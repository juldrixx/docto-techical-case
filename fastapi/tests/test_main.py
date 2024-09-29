# pylint: disable=redefined-outer-name
"""
Test module for FastAPI endpoints related to Todo items.
"""
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
import pytest
from main import app, get_db
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
