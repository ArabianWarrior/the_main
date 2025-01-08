from pydantic import BaseModel, ConfigDict
from datetime import date


class BookingsAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int

    
class BookingsAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class Bookings(BookingsAdd):

    id: int
    model_config = ConfigDict(from_attributes=True)


class BookingsPatch(BaseModel):
    user_id: int | None = None
    room_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None
    price: int | None = None
