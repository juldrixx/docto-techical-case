from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
import pytest
from main import app, get_db
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture
def db_session_mock():
    db_mock = MagicMock(spec=Session)
    yield db_mock


@pytest.fixture(autouse=True)
def override_get_db(db_session_mock):
    app.dependency_overrides[get_db] = lambda: db_session_mock


def test_main_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello, this message comes from the Fast API root endpoint!"


# def test_get_todos(db_session_mock):
#     # Mock the CRUD function to return predefined values
#     mock_todos = [{"id": 1, "label": "Test Todo", "quantity": 1}]
#     db_session_mock.query.return_value.offset.return_value.limit.return_value.all.return_value = mock_todos
#     db_session_mock.query.return_value.count.return_value = 1

#     with patch("database.crud.get_todos", return_value=(1, mock_todos)):
#         response = client.get("/todos?skip=0&limit=10")

#     assert response.status_code == 200
#     assert response.json() == {
#         "total": 1,
#         "todos": mock_todos
#     }


# def test_post_todo_success(db_session_mock):
#     new_todo_data = {
#         "label": "New Todo",
#         "quantity": 1
#     }
#     created_todo = {
#         "id": 1,
#         "label": "New Todo",
#         "quantity": 1
#     }

#     with patch("database.crud.create_todo", return_value=created_todo):
#         response = client.post("/todos", json=new_todo_data)

#     assert response.status_code == 200
#     assert response.json() == created_todo


# def test_delete_todo_success(db_session_mock):
#     todo_id = 1
#     todo_item = {
#         "id": todo_id,
#         "label": "Test Todo",
#         "quantity": 0
#     }

#     with patch("database.crud.delete_todo", return_value=todo_item):
#         response = client.delete(f"/todos/{todo_id}")

#     assert response.status_code == 200
#     assert response.json() == todo_item


# def test_delete_todo_not_found(db_session_mock):
#     todo_id = 999

#     # Simulate NoResultFound exception being raised
#     with patch("database.crud.delete_todo", side_effect=NoResultFound):
#         response = client.delete(f"/todos/{todo_id}")

#     assert response.status_code == 404
#     assert response.json() == {"detail": "Todo not found"}
