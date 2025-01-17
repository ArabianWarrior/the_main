from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomWithRels

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            data_from: date,
            data_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(data_from, data_to, hotel_id)
        query = (
        select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model) for model in result.unique().scalars().all()]
    
    async def get_room_with_facilities(self, room_id: int):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id == room_id)
        )
        result = await self.session.execute(query)
        room = result.scalars().one_or_none()
        return RoomWithRels.model_validate(room)