from fastapi import FastAPI

from app.taski.routers import taski_router


app = FastAPI(summary='Менеджер задач')


@app.get('/')
async def home_page():
    return {
        'message': 'Главная страница'
    }


app.include_router(taski_router)
