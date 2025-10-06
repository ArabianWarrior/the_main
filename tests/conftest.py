# conftest.py — замените содержимое на это (копипаст)
import json
import os
# Устанавливаем TEST mode ДО любых импортов из src
os.environ["MODE"] = "TEST"

import pytest
from httpx import AsyncClient, ASGITransport

from src.models import *
from src.config import settings
from src.main import app

from src.database import Base, engine_null_pool

#Pytest фикстуры позволяют
#1) Подготавливать окружение и инфраструктуру для тестов
#2) переиспользовать часто используемые данные (Сессия к Бд/ мок данные и др)

@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"



@pytest.fixture(scope="session",autouse=True)
#Для того чтобы не прогонялись все тесты сразу
#Мы будем использовать scope="session", то у нас будет запускаться
#Тот тест, который мы запустили, а остальные будут в спячке
async def setup_database():
    #Пишем здесь assert, если assert не сработает
    #То никакой код дальше не сработает
    print("Я ФИКСТУРА")
    assert settings.MODE == "TEST"
    
    async with engine_null_pool.begin() as conn:
        #у нас будут дропаться таблицы, только если мы будем
        #в тестовом окружении
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture           
async def add_data_json():
        #прочтем данные обоих файлов
        with open("src/tests/mock_hotels.json", encoding="utf-8") as f:
            hotels_data = json.load(f)
        
        with open("src/tests/mock_rooms.json", encoding="utf-8") as f:
            rooms_data = json.load(f)
        
        #вернем данные чтобы их можно было использовать в тестах
        return {
            "hotels": hotels_data,
            "rooms": rooms_data
        }


#pytest, автоматически запускает все фикстуры, у которых стоит autouse=True
@pytest.fixture(scope="session", autouse=True)
async def add_register_user(setup_database):
   #Создаем асинхронный клиет для нашего API
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
            await ac.post(
                "/auth/register",
                json={
                "email": "baby@mail.com",
                "password": "1234"}
            )
