from sqlalchemy import delete, select
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import  Facility, RoomsFacility, RoomsFacilityAdd

class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacility

    async def update_facilities(self, room_id: int, new_facilities_ids: list[int]) -> None:
        # Получаем текущие удобства для номера
        current_facilities_query = select(self.model).filter_by(room_id=room_id)
        current_facilities = await self.session.execute(current_facilities_query)
        current_facilities_ids = [facility.facility_id for facility in current_facilities.scalars().all()]

        # Определяем, какие удобства нужно удалить и какие добавить
        facilities_to_add = list(set(new_facilities_ids) - set(current_facilities_ids))
        facilities_to_remove = list(set(current_facilities_ids) - set(new_facilities_ids))

        # Удаляем старые удобства
        if facilities_to_remove:
            delete_stmt = delete(self.model).filter(self.model.room_id == room_id, self.model.facility_id.in_(facilities_to_remove))
            await self.session.execute(delete_stmt)

        # Добавляем новые удобства
        rooms_facilities_to_add = [RoomsFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in facilities_to_add]
        if rooms_facilities_to_add:
            await self.add_bulk(rooms_facilities_to_add)

        await self.session.commit()

