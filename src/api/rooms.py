from fastapi import APIRouter, Body, HTTPException
from src.schemas.rooms import Rooms, RoomsAdd, RoomsAddRequest, RoomsPatch, RoomsPatchRequest
from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker



router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms")
async def get_all_rooms():
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all()
        return rooms

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Комната не найдена")
        return room

@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, room_data: RoomsAddRequest = Body()):
    _room_data = RoomsAdd(hotel_id = hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    
    return {"status": "OK", "data": room}

@router.put("/{hotel_id}/rooms/{room_id}")
async def replace_room(hotel_id, room_id: int, room_data: RoomsAddRequest):
    _room_data = RoomsAdd(hotel_id = hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=id)
        if not room:
            raise HTTPException(status_code=404, detail="Комната не найдена")
        
        await RoomsRepository(session).edit(_room_data, id=room_id)
        updated_room = await RoomsRepository(session).get_one_or_none(id=id)
        await session.commit()
    
    return updated_room

@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
        hotel_id: int,
        room_id: int, 
        room_data: RoomsPatchRequest
):
       
    _room_data = RoomsPatch(hotel_id = hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:

        await RoomsRepository(session).edit(
            _room_data, 
            exclude_unset=True, 
            id=room_id, 
            hotel_id=hotel_id)
        await session.commit()

        return {"status": "OK"}

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id,hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}