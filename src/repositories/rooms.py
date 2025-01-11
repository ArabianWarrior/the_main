from datetime import date


from repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
        self,
        hotel_id: int | None,
        data_from: date,
        data_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(data_from, data_to, hotel_id)
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))