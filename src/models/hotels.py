from sqlalchemy.orm import  mapped_column, Mapped
from sqlalchemy import String
from src.database import Base


class HotelsOrm(Base):
    __tablename__ = "hotels"
    __table_args__ = {"extend_existing": True}
   

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=100))
    location: Mapped[str] 
    