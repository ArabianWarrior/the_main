from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database import Base

class FacilitiesOrm(Base):
    __tablename__ = "facilities"
    __table_args__ = {"extend_existing": True}

    id: Mapped [int] = mapped_column(primary_key=True)
    title: Mapped [str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="facilities",
        secondary = "rooms_facilities",
    )

class RoomsFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"
    __table_args__ = {"extend_existing": True}

    id: Mapped [int] = mapped_column(primary_key=True)
    room_id: Mapped [int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped [int] = mapped_column(ForeignKey("facilities.id"))