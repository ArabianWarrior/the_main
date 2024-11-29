from fastapi import  Query, APIRouter, Body
from shemas.hotels import Hotel, HotelIPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
        {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("/",summary="Получение отелей")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
        page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=50, description="Количество отелей на странице"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    
    start = (page - 1) * per_page
    end = start + per_page
    paginated_hotels = hotels_[start:end]

    return {
        "total_items": len(hotels_),  # Общее количество элементов после фильтрации
        "page": page,
        "per_page": per_page,
        "total_pages": (len(hotels_) + per_page - 1) // per_page,  # Округление вверх
        "data": paginated_hotels,
    }
    
    


@router.post("/",summary="Создать отель")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "name": "sochi y morya",
    }},
    "2": {"summary": "Москва", "value": {
        "title": "Отель Москва у  красной площади", 
        "name": "Moscow y red square",
    }},
}),
):
    
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
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

@router.delete("/{hotel_id}", summary="Удалить отель")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
