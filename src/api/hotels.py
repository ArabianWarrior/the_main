from fastapi import  Query, APIRouter, Body

from sqlalchemy import Engine, insert, select

from models.hotels import HotelsOrm

from src.api.dependecies import PaginationDep
from src.shemas.hotels import Hotel, HotelIPatch
from src.database import async_session_maker
from src.database import engine


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/",summary="Получение отелей")
async def get_hotels(
        pagination: PaginationDep,
        id: str | None = Query(None, description="Айдишник"),
        location: str | None = Query(None, description="Местополежние отеля"),
        title: str | None = Query(None,description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.ilike(f"%{location}%"))
        if title:
            query = query.filter(HotelsOrm.location.ilike(f"%{location}%"))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page-1))
        )
        
        result = await session.execute(query)
        hotels = result.scalars().all()
        
        #print(type(result), result)
        
        return hotels

    #if pagination.page and pagination.per_page:
        #return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]
   


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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Редактировать отель")
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


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
    #Проверка существует ли такой id
        query = select(HotelsOrm).filter(HotelsOrm.id == hotel_id)
        result = await session.execute(query)
        hotel = result.scalars().first()
        if not hotel:
            raise HTTPException(status_code=404, detail="Отель не найден")
    
        await session.delete(hotel)
        await session.commit
        return {"status": "OK"}
