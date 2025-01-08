from fastapi import APIRouter, Body
from src.schemas.bookings import  BookingsAdd
from src.api.dependecies import  DBDep


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def add_booking(db: DBDep,booking_data: BookingsAdd = Body()):
    booking = await db.bookings.create_booking(booking_data)
    await db.commit()
    return {"status": "OK", "id": booking}
    