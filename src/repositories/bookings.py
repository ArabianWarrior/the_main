from repositories.base import BaseRepository
from schemas.bookings import Bookings
from src.models.bookings import BookingsOrm



class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Bookings
