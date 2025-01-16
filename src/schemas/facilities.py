from pydantic import BaseModel, ConfigDict, Field



class FacilitiesAdd(BaseModel):
    title: str



class Facility(FacilitiesAdd):
    id: int
    
    model_config = ConfigDict(from_attributes=True)



class RoomsFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomsFacility(RoomsFacilityAdd):
    id: int


class RoomsFacilityPatch(BaseModel):
    title: str | None = Field(None)
    room_id: int | None = Field(None)