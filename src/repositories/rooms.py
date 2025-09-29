from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.mapper.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

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
        return [RoomDataWithRelsMapper.map_to_domain_entity(model) for model in result.unique().scalars().all()]
    
    async def get_room_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomDataWithRelsMapper.map_to_domain_entity(model)