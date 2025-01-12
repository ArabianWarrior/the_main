from pydantic import BaseModel, ConfigDict



class TheFacilitiesAdd(BaseModel):
    title: str



class TheFacilities(TheFacilitiesAdd):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
