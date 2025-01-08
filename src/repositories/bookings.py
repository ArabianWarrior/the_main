from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


class BookingsRepository:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def create_booking(self, room_id: int, date_from, date_to) -> BookingsOrm:
        async with self.db.begin():
            result = await self.db.execute(select(RoomsOrm).filter(RoomsOrm.id == room_id))
            room = result.scalars().first()
            if not room:
                raise ValueError(f"Room with id {room_id} not found.")

            booking = BookingsOrm(
                room_id=room_id,
                date_from=date_from,
                date_to=date_to,
                price=room.price,
            )
            self.db.add(booking)
        return booking