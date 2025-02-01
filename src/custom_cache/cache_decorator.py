import functools
import json
import hashlib
from fastapi import Request
from typing import Callable
from fastapi.encoders import jsonable_encoder  # Импортируем для сериализации
from src.connectors.redis_connector import RedisManager

# Инициализируем менеджер Redis с нужными параметрами
redis_manager = RedisManager(host="localhost", port=6379)

def custom_cache(expire: int = 10):
    """
    Декоратор для кэширования результата функции с помощью Redis.
    expire: время жизни кэша в секундах.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Если объект Request передается через kwargs, используем его
            request: Request = kwargs.get("request")
            if not request:
                # Если Request отсутствует, просто вызываем оригинальную функцию
                return await func(*args, **kwargs)
            
            # Проверяем, подключён ли Redis; если нет — подключаемся
            if not redis_manager.redis:
                await redis_manager.connect()

            # Генерируем уникальный ключ для кэша
            cache_key = generate_cache_key(request)

            # Пытаемся получить данные из кэша
            cached_data = await redis_manager.get(cache_key)
            if cached_data:
                print(f"Извлекаем данные из кэша для ключа: {cache_key}")
                return json.loads(cached_data)
            
            # Если в кэше данных нет, вызываем оригинальную функцию
            response = await func(*args, **kwargs)

            # Преобразуем response в JSON-сериализуемый формат
            encoded_response = jsonable_encoder(response)
            
            # Сохраняем результат в кэше, сериализуя в JSON
            await redis_manager.set(cache_key, json.dumps(encoded_response), expire)
            return response
        return wrapper 
    return decorator

def generate_cache_key(request: Request) -> str:
    """
    Генерирует уникальный ключ для кэша на основе URL-пути и query параметров.
    """
    path = request.url.path
    # Сортируем query-параметры для единообразия
    query_params = sorted(request.query_params.items())
    query_string = "&".join(f"{k}={v}" for k, v in query_params)
    full_key = f"{path}?{query_string}"
    # Хэшируем строку для получения компактного ключа
    return hashlib.sha256(full_key.encode()).hexdigest()
