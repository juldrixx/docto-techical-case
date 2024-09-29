# pylint: disable=redefined-outer-name
"""
Unit tests for the CRUD operations related to the Todo model.
"""
from unittest.mock import MagicMock, create_autospec
import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from database import crud, models, schemas


@pytest.fixture
def mock_db_session():
    """
    Fixture to create a mock database session.

    Returns:
        A mock `Session` object from SQLAlchemy's ORM.
    """
    return create_autospec(Session)


def test_get_todos(mock_db_session):
    """
    Test the `get_todos` function from the `crud` module.

    Simulates fetching todos from the database and verifies that the correct 
    number of todos is returned, and that their properties match the expected values.

    Args:
        mock_db_session (Session): The mock database session.
    """
    mock_todos = [models.Todo(id=1, label="Test Todo 1", quantity=1), models.Todo(
        id=2, label="Test Todo 2", quantity=2)]
    query = mock_db_session.query
    query.return_value.offset.return_value.limit.return_value.all.return_value = mock_todos
    query.return_value.count.return_value = len(mock_todos)

    total_count, todos = crud.get_todos(db=mock_db_session)

    assert total_count == 2
    assert len(todos) == 2
    assert todos[0].label == "Test Todo 1"
    assert todos[1].label == "Test Todo 2"
    assert todos[0].quantity == 1
    assert todos[1].quantity == 2


def test_create_todo(mock_db_session):
    """
    Test the `create_todo` function from the `crud` module.

    Verifies that a new Todo can be created and checks if the database session
    methods (add, commit, refresh) are called as expected. It also checks if the
    returned Todo object has the correct values including an auto-assigned id.

    Args:
        db_session (Session): The mock database session.
    """
    new_todo = schemas.TodoCreate(label="New Todo", quantity=0)
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()

    def mock_refresh(todo):
        todo.id = 1
    mock_db_session.refresh.side_effect = mock_refresh

    created_todo = crud.create_todo(db=mock_db_session, todo=new_todo)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert created_todo.label == "New Todo"
    assert created_todo.quantity == 0
    assert created_todo.id == 1


def test_delete_todo_success(mock_db_session):
    """
    Test the `delete_todo` function from the `crud` module when the Todo exists.

    Simulates the successful deletion of a Todo from the database and verifies
    that the correct methods (query, delete, commit) are called, and the correct
    Todo object is deleted.

    Args:
        mock_db_session (Session): The mock database session.
    """
    mock_todo = models.Todo(id=1, label="Test Todo", quantity=0)
    mock_db_session.query.return_value.filter.return_value.one.return_value = mock_todo
    mock_db_session.delete = MagicMock()
    mock_db_session.commit = MagicMock()

    deleted_todo = crud.delete_todo(db=mock_db_session, todo_id=1)

    mock_db_session.query.return_value.filter.assert_called_once()
    mock_db_session.delete.assert_called_once_with(mock_todo)
    mock_db_session.commit.assert_called_once()
    assert deleted_todo.id == 1


def test_delete_todo_not_found(mock_db_session):
    """
    Test the `delete_todo` function from the `crud` module when the Todo does not exist.

    Simulates the scenario where the Todo with the given id does not exist in the database,
    and verifies that a `NoResultFound` exception is raised.

    Args:
        mock_db_session (Session): The mock database session.
    """
    mock_db_session.query.return_value.filter.return_value.one.side_effect = NoResultFound

    with pytest.raises(NoResultFound):
        crud.delete_todo(db=mock_db_session, todo_id=999)
