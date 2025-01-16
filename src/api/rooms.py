from datetime import date
from fastapi import APIRouter, Body, Query


from src.schemas.facilities import RoomsFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch
from src.api.dependecies import DBDep




router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int, 
        db: DBDep,
        data_from: date = Query(example="2025-01-01"),
        data_to: date = Query(example="2025-01-05"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id,data_from=data_from,data_to=data_to)

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
        return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)

@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, room_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    
    rooms_facilities_data = [RoomsFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilites_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}

@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(db: DBDep,hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    
    if room_data.facilites_ids is not None:
        await db.rooms_facilities.update_facilities(room_id, room_data.facilites_ids)
    await db.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)

    if room_data.facilites_ids is not None:
        await db.rooms_facilities.update_facilities(room_id, room_data.facilites_ids)

    await db.commit()

    return {"status": "OK"}

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}