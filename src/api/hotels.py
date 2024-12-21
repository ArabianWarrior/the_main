from fastapi import  Query, APIRouter, Body

from sqlalchemy import Engine, insert, select, func

from models.hotels import HotelsOrm

from repositories.hotels import HotelsRepository
from src.api.dependecies import PaginationDep
from src.shemas.hotels import Hotel, HotelIPatch
from src.database import async_session_maker
from src.database import engine


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/",summary="Получение отелей")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None,description="Название отеля"),
):
        per_page = pagination.per_page or 5
        async with async_session_maker() as session:
            return await HotelsRepository(session).get_all(
                location = location,
                title = title, 
                limit= per_page, 
                offset= per_page * (pagination.page - 1)
            )
        
        
@router.post("/",summary="Создать отель")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", 
          "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "location": "ул. Лермонтова, 1",
    }},
    "2": {"summary": "Москва", 
          "value": {
            "title": "Отель Москва у  красной площади", 
            "location": "ул. Пушкина, 5",
    }},
}),
):
   async with async_session_maker() as session:
       hotel = await HotelsRepository(session).add(hotel_data)
       await session.commit()
   return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Редактировать отель")
async def edit_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        repository = HotelsRepository(session)
        
        if hotel_data.title:
            await repository.update_title(hotel_id, hotel_data.title)
        
        if hotel_data.location:
            await repository.update_location(hotel_id, hotel_data.location)
        
        await session.commit()

    return {"status": "OK", "message": "Hotel updated successfully"}
        


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelIPatch
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}

@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int):
   async with async_session_maker() as session:
        hotel_repo = HotelsRepository(session)
        await hotel_repo.delete_hotel(hotel_id)
        await session.commit()
   return {"status": "OK", "message": "Hotel deleted successfully"}
