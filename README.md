# Авторизация на FastAPI.
Описание проекта:
Описание проекта
Tasks Manager — веб-приложение, разработанное с использованием фреймворка FastAPI
Оно позволяет создавать, редактировать, просматривать и удалять различные задачи.

# Стек технологий

1. **Backend**
   - Python 3.12
   - FastAPI: высокопроизводительный веб-фреймворк для быстрого написания RESTful API.
   - SQLAlchemy: библиотека Python для взаимодействия с базами данных.
   - PostgreSQL: реляционная база данных для хранения всех сущностей приложения.
   - Pytest: модуль тестирования и автоматизацию функциональности приложений.

# Запуск:
Локально -
1. Установка зависимостей - pip install -r requirements.txt
2. Создайте базу данных PostgreSQL и настройте константу - "DATABASE_URL" для подключение через .env файл.
3. Выполните миграцию базы данных:
4. alembic init -t async app/migrations
5. alembic revision --autogenerate -m "Initial migration"
6. alembic upgrade head
7. uvicorn app.main:app
8. Откройте API в браузере: http://localhost:8000/docs
9. перейдите к тестированию эндпоинтов.


Dockerfile:
1. сбилдить образ: docker build -t appfastapi .
2. собрать и запустить в контейнер: docker run -d -p 8000:80 --name fastapi appfastapi
3. перейти на адрес с документации к API для теста: http://localhost:8000/docs
