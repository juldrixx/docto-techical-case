from unittest.mock import MagicMock, create_autospec
import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from database import crud, models, schemas


@pytest.fixture
def db_session():
    """Fixture to create a mock database session."""
    return create_autospec(Session)


def test_get_todos(db_session):
    mock_todos = [models.Todo(id=1, label="Test Todo 1", quantity=1), models.Todo(
        id=2, label="Test Todo 2", quantity=2)]
    db_session.query.return_value.offset.return_value.limit.return_value.all.return_value = mock_todos
    db_session.query.return_value.count.return_value = len(mock_todos)

    total_count, todos = crud.get_todos(db=db_session)

    assert total_count == 2
    assert len(todos) == 2
    assert todos[0].label == "Test Todo 1"
    assert todos[1].label == "Test Todo 2"
    assert todos[0].quantity == 1
    assert todos[1].quantity == 2


def test_create_todo(db_session):
    new_todo = schemas.TodoCreate(label="New Todo", quantity=0)
    db_session.add = MagicMock()
    db_session.commit = MagicMock()

    def mock_refresh(todo):
        todo.id = 1
    db_session.refresh.side_effect = mock_refresh

    created_todo = crud.create_todo(db=db_session, todo=new_todo)

    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once()
    assert created_todo.label == "New Todo"
    assert created_todo.quantity == 0
    assert created_todo.id == 1


def test_delete_todo_success(db_session):
    mock_todo = models.Todo(id=1, label="Test Todo", quantity=0)
    db_session.query.return_value.filter.return_value.one.return_value = mock_todo
    db_session.delete = MagicMock()
    db_session.commit = MagicMock()

    deleted_todo = crud.delete_todo(db=db_session, todo_id=1)

    db_session.query.return_value.filter.assert_called_once()
    db_session.delete.assert_called_once_with(mock_todo)
    db_session.commit.assert_called_once()
    assert deleted_todo.id == 1


def test_delete_todo_not_found(db_session):
    db_session.query.return_value.filter.return_value.one.side_effect = NoResultFound

    with pytest.raises(NoResultFound):
        crud.delete_todo(db=db_session, todo_id=999)
