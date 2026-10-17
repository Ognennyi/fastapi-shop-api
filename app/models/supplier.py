from uuid import UUID, uuid4

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[UUID] = mapped_column( 
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4)

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    address_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("addresses.id"),
        nullable=False,
        unique=True
    )

    phone_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )


    address: Mapped["Address"] = relationship(
        "Address",
        back_populates="supplier"
    )


    products: Mapped[list["Product"]] = relationship(
    "Product",
    back_populates="supplier",
)