from fastapi import APIRouter, Query

from src.api.dependecies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAddRequest, BookingsAdd


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingsAddRequest,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingsAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get("")
async def all_bookings(
    db: DBDep,
    room_id: int | None = Query(None)
):
    return await db.bookings.get_all(room_id=room_id)

@router.get("/me")
async def only_me(
    db: DBDep,
    room_id: int
):
    return await db.bookings.get_filtered(room_id=room_id)