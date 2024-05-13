import asyncpg
import pytest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'dish_api_service/app'))
sys.path.append(str(BASE_DIR / 'dish_service/app'))

from dish_api_service.app.main import service_alive as dish_api_status
from dish_service.app.main import service_alive as dish_status


@pytest.mark.asyncio
async def test_database_connection():
    try:
        connection = await asyncpg.connect('postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query')
        assert connection
        await connection.close()
    except Exception as e:
        assert False, f"Не удалось подключиться к базе данных: {e}"


@pytest.mark.asyncio
async def test_dish_api_service_connection():
    r = await dish_api_status()
    assert r == {'message': 'Service alive'}


@pytest.mark.asyncio
async def test_dish_service_connection():
    r = await dish_status()
    assert r == {'message': 'Service alive'}
