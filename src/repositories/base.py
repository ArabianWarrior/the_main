from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

class BaseRepository:
    model = None
    
    def __init__(self, session):
        self.session = session
        
    
    
    async def get_all(self, *args, **kwargs):
            query = select(self.model)
            result = await self.session.execute(query)
            return result.scalars().all()


    async def get_one_or_none(self, **filter_by):
            query = select(self.model).filter_by(**filter_by)
            result = await self.session.execute(query)
            return result.scalars().one_or_none()


    async def add(self, data: BaseModel):
          add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
          result = await self.session.execute(add_data_stmt)
          return result.scalars().one()


    async def update_title(self, hotel_id: int, title: str):
        data = {'title': title}
        update_tit = (
            update(self.model)
            .where(self.model.id == hotel_id)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(update_tit)
        return result.scalars().one_or_none()

    async def update_location(self, hotel_id: int, location: str):
        data = {'location': location}
        update_loc = (
            update(self.model)
            .where(self.model.id == hotel_id)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(update_loc)
        return result.scalars().one_or_none()

    async def delete_hotel(self, model, hotel_id: int) -> None:
         delete_stmt = delete(model).where(model.id == hotel_id)
         await self.session.execute(delete_stmt)
   