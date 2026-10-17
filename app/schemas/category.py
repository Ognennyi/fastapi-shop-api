from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID


class CategoryCreate(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Monitors"
            }
        }
    )

    name: str = Field(min_length=1, max_length=50)


class CategoryResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Monitors"
            }
        }
    )

    id: UUID
    name: str = Field(min_length=1, max_length=50)
