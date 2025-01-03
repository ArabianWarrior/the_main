from fastapi import APIRouter, HTTPException
from src.schemas.rooms import Rooms, RoomsAdd, RoomsUpdate
from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.repositories.base import BaseRepository


router = APIRouter(prefix="/rooms", tags=["Номера"])

@router.get("/")
async def get_all_rooms():
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all()
        return rooms

@router.get("/{id}", response_model=Rooms)
async def get_room(id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=id)
        if not room:
            raise HTTPException(status_code=404, detail="Комната не найдена")
        return room

@router.post("/", response_model=Rooms)
async def create_room(room_data: RoomsAdd):
    async with async_session_maker() as session:
        new_room = await RoomsRepository(session).add(room_data)
        return new_room

@router.put("/{id}", response_model=Rooms)
async def replace_room(id: int, room_data: RoomsAdd):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=id)
        if not room:
            raise HTTPException(status_code=404, detail="Комната не найдена")
        
        await RoomsRepository(session).edit(room_data, id=id)
        updated_room = await RoomsRepository(session).get_one_or_none(id=id)
        return updated_room

@router.patch("/{id}", response_model=Rooms)
async def update_room(id: int, room_data: RoomsUpdate):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=id)
        if not room:
            raise HTTPException(status_code=404, detail="Комната не найдена")

        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=id)
        updated_room = await RoomsRepository(session).get_one_or_none(id=id)
        return updated_room

@router.delete("/{id}")
async def delete_room(id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=id)
        await session.commit()
    return {"status": "OK"}