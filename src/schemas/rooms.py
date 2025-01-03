from pydantic import BaseModel, Field, ConfigDict


class RoomsAdd(BaseModel):
    title: str
    description: str
    price: float
    quantity: int


class Rooms(RoomsAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomsUpdate(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: float | None = Field(None)
    quantity: int | None = Field(None)