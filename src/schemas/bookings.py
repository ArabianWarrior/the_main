from pydantic import BaseModel, ConfigDict
from datetime import date


class BookingsAddRequest(BaseModel):
    room_id: int
    data_from: date
    data_to: date


class BookingsAdd(BaseModel):
    user_id: int
    room_id: int
    data_from: date
    data_to: date
    price: int


class Bookings(BookingsAdd):
    id: int
    
    model_config = ConfigDict(from_attributes=True)



