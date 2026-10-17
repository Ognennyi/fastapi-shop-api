from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID


class AddressCreate(BaseModel):
    country: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    street: str = Field(min_length=1, max_length=255)

class AddressResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    country: str
    city: str
    street: str