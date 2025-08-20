from typing import Literal

from pydantic import BaseModel, Field


class CreateTaski(BaseModel):
    """Модель для создания задачи."""

    name: str = Field(max_length=50, title='Название задачи')
    description: str = Field(max_length=2000, title='Описание задачи')
    status: Literal['Создано', 'В работе', 'Выполнено'] = Field(
        title='Статус задачи',
        description='Возможные статусы: Создано, В работе, Выполнено.'
    )

    model_config = dict(
        json_schema_extra={
            'examples': [
                {
                    'name': 'Новая задача',
                    'description': 'Краткое описание новой задачи.',
                    'status': 'Создано'
                }
            ]
        }
    )
