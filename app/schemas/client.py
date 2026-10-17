from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

from typing import Literal

from app.schemas.address import AddressCreate


class ClientCreate(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "client_name": "Ivan",
                "client_surname": "Ivanov",
                "birthday": "2000-05-15",
                "gender": "M",
                "address": {
                    "country": "Russia",
                    "city": "Kazan",
                    "street": "Baumana 10"
                }
            }
        }
    )


    client_name : str = Field(min_length=1, max_length=50)
    client_surname : str = Field(min_length=1, max_length=50)
    birthday : date
    gender : Literal["M", "F"]
    address : AddressCreate

class ClientResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "client_name": "Ivan",
                "client_surname": "Ivanov",
                "birthday": "2000-05-15",
                "gender": "M",
                "registration_date": "2026-10-17T13:30:00+03:00",
                "address_id": "660e8400-e29b-41d4-a716-446655440000"
            }
        }
    )

    id: UUID
    client_name : str
    client_surname : str
    birthday : date
    gender : str
    registration_date: datetime
    address_id : UUID

class ClientAddressUpdate(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "country": "Russia",
                "city": "Kazan",
                "street": "Chistopolskaya 20"
            }
        }
    )

    country: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    street: str = Field(min_length=1, max_length=255)