from sqlalchemy.orm import  mapped_column, Mapped
from sqlalchemy import Integer, ForeignKey
from src.database import Base

from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property


class BookingsOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column (ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column (ForeignKey("rooms.id"))
    data_from: Mapped[date]
    data_to: Mapped[date] 
    price: Mapped[int] 

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days