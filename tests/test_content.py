import pytest

from fastapi import status

from sqlalchemy.exc import IntegrityError, DBAPIError


from app.taski.models import Taski, StatusEnum


@pytest.mark.asyncio
async def test_task_creation_without_name_should_fail(db_session):
    """Тест: создание задачи без имени должно вызывать IntegrityError"""

    task = Taski(
        description='Test Description',
        status=StatusEnum.create
    )
    db_session.add(task)

    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_task_creation_without_description_should_fail(db_session):
    """Тест: создание задачи без описания должно вызывать IntegrityError"""

    task = Taski(
        name='Test Task',
        status=StatusEnum.create
    )
    db_session.add(task)

    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_task_creation_with_valid_data(db_session):
    """Тест создания задачи с валидными данными"""

    task = Taski(
        name='Test Task',
        description='Test Description',
        status=StatusEnum.create
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    assert task.id is not None
    assert task.uuid is not None
    assert task.created_at is not None


@pytest.mark.asyncio
async def test_task_name_length_validation(db_session):
    """Тест валидации длины имени"""

    task = Taski(
        name='A' * 51,
        description='Test',
        status=StatusEnum.create
    )
    db_session.add(task)

    with pytest.raises(DBAPIError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_invalid_status(client_db):
    """ Проверка обработки ситуации, когда вводится недопустимый статус. """

    invalid_task_data = {
        'name': 'new_task',
        'description': 'new_description',
        'status': 'Некорректный_статус'
    }

    create_response = await client_db.post('/taski/', json=invalid_task_data)

    assert create_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    error_message = create_response.json().get('detail')[0].get('msg')
    expected_error_msg = "Input should be 'Создано', 'В работе' or 'Выполнено'"

    # Проверяем, что сервер возвращает ожидаемое сообщение об ошибке
    assert error_message == expected_error_msg
