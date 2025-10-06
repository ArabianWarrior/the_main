from src.schemas.hotels import HotelAdd, Hotel
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool

#Проверка ручки на добавление отеля
async def test_add_hotel():
    hotel_data = HotelAdd(title="Hotel 10 stars", location="Дубай")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        new_hotel_data = await db.hotels.add(hotel_data)
        await db.commit()
        print(f"{new_hotel_data=}")


