from fastapi import APIRouter
from src.api.dependecies import DBDep
from fastapi_cache.decorator import cache
from src.schemas.facilities import FacilitiesAdd
from fastapi import Body

from src.tasks.the_tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("ИДУ В БАЗУ ДАННЫХ")
    return await db.facilities.get_all()
      
@router.post("")
@cache(expire=10)
async def create_facilities(db: DBDep, facilities_data: FacilitiesAdd = Body()):
    facility = await db.facilities.add(facilities_data)
    await db.commit()
    
    test_task.delay()

    return {"status": "OK", "data": facility}
