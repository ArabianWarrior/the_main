from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.repositories.mapper.mappers import BookingDataMapper
from src.models.bookings import BookingsOrm
from datetime import date



class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_check_in(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.data_from == date.today())
        )
        res = self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]