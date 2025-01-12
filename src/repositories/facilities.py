from src.models.facilities import Facilities
from src.repositories.base import BaseRepository
from src.schemas.facilities import TheFacilities

class FacilitiesRepository(BaseRepository):
    model = Facilities
    schema = TheFacilities
