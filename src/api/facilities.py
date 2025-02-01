from fastapi import APIRouter, Request
from src.api.dependecies import DBDep
from src.custom_cache.cache_decorator import custom_cache
from src.schemas.facilities import FacilitiesAdd
from fastapi import Body

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
@custom_cache(expire=10)
async def get_facilities(request: Request, db: DBDep):
    print("ИДУ В БАЗУ ДАННЫХ")
    return await db.facilities.get_all()
      
@router.post("")
async def create_facilities(db: DBDep, facilities_data: FacilitiesAdd = Body()):
    facility = await db.facilities.add(facilities_data)
    await db.commit()
    return {"status": "OK", "data": facility}
