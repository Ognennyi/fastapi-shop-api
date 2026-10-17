from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from decimal import Decimal


class ProductCreate(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Samsung 33",
                "category_id": "550e8400-e29b-41d4-a716-446655440000",
                "price": 74990.00,
                "available_stock": 12,
                "supplier_id": "660e8400-e29b-41d4-a716-446655440000",
            }
        }
    )

    name : str = Field(min_length=1, max_length=100)
    category_id: UUID
    price : Decimal = Field(ge=0)
    available_stock : int = Field(ge=0)
    supplier_id: UUID


class ProductResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "770e8400-e29b-41d4-a716-446655440000",
                "name": "Samsung 33",
                "category_id": "550e8400-e29b-41d4-a716-446655440000",
                "price": 74990.00,
                "available_stock": 12,
                "last_update_date": "2026-10-17T16:00:00+03:00",
                "supplier_id": "660e8400-e29b-41d4-a716-446655440000",
                "image_id": None,
            }
        }
    )

    id: UUID
    name: str
    category_id: UUID
    price: Decimal
    available_stock: int
    last_update_date: datetime
    supplier_id: UUID
    image_id: UUID | None


class ProductStockUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "amount": 3
            }
        }
    )
    
    amount: int = Field(gt=0)