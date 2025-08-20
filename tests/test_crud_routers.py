import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_and_get_taski(client_db):
    """
    Проверка создания задачи, получение задачи и статус кода.
    """

    create_response = await client_db.post('/taski/', json=client_db.test_data)

    assert create_response.status_code == 201

    response = await client_db.get('/taski/')
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]['name'] == client_db.test_data['name']


@pytest.mark.asyncio
async def test_update_task(client_db, update_data):
    """ Тестирует обновление существующей задачи. """

    create_response = await client_db.post('/taski/', json=client_db.test_data)

    assert create_response.status_code == 201

    task_id = create_response.json()['id']

    response = await client_db.put(f'/taski/{task_id}', json=update_data)
    assert response.status_code == status.HTTP_200_OK

    read_response = await client_db.get(f'/taski/{task_id}')
    assert read_response.status_code == status.HTTP_200_OK
    updated_task = read_response.json()
    assert updated_task['name'] == update_data['name']
    assert updated_task['description'] == update_data['description']
    assert updated_task['status'] == update_data['status']


@pytest.mark.asyncio
async def test_delete_task(client_db):
    """ Тестирует удаление задачи. """

    create_response = await client_db.post('/taski/', json=client_db.test_data)
    assert create_response.status_code == 201

    task_id = create_response.json()['id']
    delete_response = await client_db.delete(f'/taski/{task_id}')
    assert delete_response.status_code == status.HTTP_200_OK

    check_response = await client_db.get(f'/taski/{task_id}')
    assert check_response.status_code == status.HTTP_404_NOT_FOUND
