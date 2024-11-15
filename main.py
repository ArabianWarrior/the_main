import json
from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import get_swagger_ui_html  # Исправленный импорт
import uvicorn
from typing import Optional

app = FastAPI()


hotels = [
    {"id": 1, "name": "Sochi", "title": "sochi",},
    {"id": 2, "name": "Dubai", "title": "dubai",},
    ]


@app.get("/hotels")
def get_holels(
    id: Optional[int] = Query(None,description="Айдишник"), #Значение по умолчанию - None
    name: Optional[str] = Query(None,description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id is not None and hotel["id"] != id:
            continue
        if name is not None and hotel["name"].lower() != name.lower():
            continue
        hotels_.append(hotel)
    return hotels_
    


#body, request body
@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1 if hotels else 1,
        "title": title,
    })
    return {"status": "OK"}

@app.patch("/hotels/{hotel_id}")
def update_hotels(
    hotel_id: int, 
    id: Optional[int] = Body(None), 
    name: Optional[str] = Body(None)):
    
    global hotels
    #Найти отель с указанным hotel_id
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            #Если передан новый id, обновить его
            if id is not None:
                hotel["id"] = id
                #Если передано новое имя, обновить его
            if name is not None:
                hotel["name"] = name
            return {"status": "updated", "hotel": hotel}
        return {"status": "error", "message": f"Hotel with id {hotel_id} not found"}, 404

@app.put("/hotels/{hotel_id}")
def change_hotel(hotel_id: int, title: str):
    global hotels
    # Найти отель с указанным id
    for hotel in hotels:
        if hotel["id"] == hotel_id:  # Используйте id для поиска
            # Обновить title, если передано новое значение
            if title:
                hotel["title"] = title
                return {"status": "updated", "hotel": hotel}
    return {"status": "error", "message": f"Hotel with id {hotel_id} not found"}

@app.delete("/hotels/{hotel_id}")
def delete_hotels(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title="Custom Docs")

if __name__ == "__main__": #эти 2 строки создаются для запуска самого сайта
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

