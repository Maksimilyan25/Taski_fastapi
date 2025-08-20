from fastapi import APIRouter, status, HTTPException

from sqlalchemy import select

from app.database.db import SessionDep
from app.taski.models import Taski
from app.schemas import CreateTaski


taski_router = APIRouter(prefix='/taski', tags=['Задачи'])


@taski_router.get('/', summary='Получение всех задач')
async def list_tasks(db: SessionDep):
    result = await db.scalars(select(Taski))
    tasks = result.all()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Список задач пуст'
        )
    return tasks


@taski_router.get('/{taski_id}', summary='Получение задачи по ID')
async def detail_taski(db: SessionDep, taski_id: int):
    taski = await db.scalar(select(Taski).where(Taski.id == taski_id))
    if not taski:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача с таким ID не найдена'
        )
    return taski


@taski_router.post(
        '/', summary='Создание задачи', status_code=status.HTTP_201_CREATED)
async def create_taski(db: SessionDep, create_taski: CreateTaski):
    try:
        taski = Taski(
            name=create_taski.name,
            description=create_taski.description,
            status=create_taski.status
        )
        db.add(taski)
        await db.commit()
        await db.refresh(taski)
        return taski

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при создании задачи: {str(e)}'
        )


@taski_router.put('/{taski_id}', summary='Обновление задачи по ID')
async def update_taski(
     db: SessionDep, update_taski: CreateTaski, taski_id: int):
    try:
        taski = await db.scalar(select(Taski).where(Taski.id == taski_id))
        if not taski:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Задача с таким ID не найдена'
            )

        taski.name = update_taski.name
        taski.description = update_taski.description
        taski.status = update_taski.status

        await db.commit()
        await db.refresh(taski)
        return taski

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при обновлении задачи: {str(e)}'
        )


@taski_router.delete('/{taski_id}', summary='Удаление задачи по ID')
async def delete_taski(db: SessionDep, taski_id: int):
    try:
        taski = await db.scalar(select(Taski).where(Taski.id == taski_id))
        if not taski:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Задача с таким ID не найдена'
            )

        await db.delete(taski)
        await db.commit()
        return {"message": "Задача удалена успешно"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при удалении задачи: {str(e)}'
        )
