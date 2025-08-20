import enum
from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Integer, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.db import Base


class StatusEnum(str, enum.Enum):
    """Класс выбора статуса задач."""

    create = 'Создано'
    in_progress = 'В работе'
    completed = 'Завершено'


class Taski(Base):
    """Модель задач.

    Хранит основную информацию про задачи.

    Attributes:
        id (int): Уникальный идентификатор задачи (первичный ключ)
        uuid (UUID): Глобально-уникальный идентификатор задачи (GUID/UUID)
        name (str): Имя задачи (макс. 50 символов, обязательное)
        description (str): Описание задачи(макс. 2000 символов, обязательное)
        status (Enum): Выбор статуса задачи(обязательное)
        created_at (datetime): Время создания задачи(текущее)
        updated_at (datetime): Время обновления задачи(текущее)
    """

    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(
        String(2000), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum), nullable=False,  default=StatusEnum.create)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
