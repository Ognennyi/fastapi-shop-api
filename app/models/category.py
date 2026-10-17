from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base



class Category(Base):
    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column( 
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4)
    
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    products: Mapped[list["Product"]] = relationship(
    "Product",
    back_populates="category",
)