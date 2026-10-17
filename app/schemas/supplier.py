from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from app.schemas.address import AddressCreate



class SupplierCreate(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "TechnoSupply",
                "phone_number": "+79991234567",
                "address": {
                    "country": "Russia",
                    "city": "Kazan",
                    "street": "Prospekt Pobedy 25"
                }
            }
        }
    )

    name: str = Field(min_length=1, max_length=150)
    phone_number: str = Field(min_length=1, max_length=30)
    address: AddressCreate

class SupplierResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "TechnoSupply",
                "address_id": "660e8400-e29b-41d4-a716-446655440000",
                "phone_number": "+79991234567"
            }
        }
    )

    id: UUID
    name: str
    address_id: UUID
    phone_number: str

class SupplierAddressUpdate(BaseModel):

    model_config = ConfigDict(
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
