from sqlalchemy import select, func
from repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Rooms, RoomsAdd, RoomsUpdate

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def add(self, room_data: RoomsAdd):
        new_room = RoomsOrm(
            title=room_data.title,
            description=room_data.description,
            price=room_data.price,
            quantity=room_data.quantity
        )
        self.session.add(new_room)
        await self.session.commit()
        return new_room

    async def get_rooms(self, hotel_id: int):
        query = select(self.model).filter(self.model.hotel_id == hotel_id)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_available_rooms(self, hotel_id: int, min_price: int = 0, max_price: int = 8000):
        query = (
            select(self.model)
            .filter(self.model.hotel_id == hotel_id)
            .filter(self.model.price >= min_price, self.model.price <= max_price)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def update_rooms(self, room_id: int, data: RoomsUpdate):
        await self.edit(data, id=room_id)