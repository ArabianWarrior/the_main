from datetime import date
from fastapi import Query, APIRouter, Body
from src.api.dependecies import PaginationDep, DBDep
from src.schemas.hotels import  HotelAdd, HotelPATCH

from fastapi_cache.decorator import cache 

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),
        data_from: date = Query(example="2025-01-01"),
        data_to: date = Query(example="2025-01-05"),
 ):
    per_page = pagination.per_page or 5
    
    return await db.hotels.get_filtered_by_time(
        data_from=data_from,
        data_to=data_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )

@router.get("/{hotel_id}")
@cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)

@router.post("")
@cache(expire=10)
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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
    await db.hotels.add(hotel_data)
    await db.commit()
   
@router.put("/{hotel_id}", summary="Редактировать отель")
@cache(expire=10)
async def edit_hotel(hotel_id: int, db: DBDep):
    await db.hotels.edit(id=hotel_id)  
    await db.commit()
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
@cache(expire=10)
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
        db: DBDep,
):
    await db.hotels.edit(hotel_data, exlcude_unset = True, id = hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.delete("/{hotel_id}", summary="Удаление отеля")
@cache(expire=10)
async def delete(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}