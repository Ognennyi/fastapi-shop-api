from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    street: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    client: Mapped["Client | None"] = relationship(
        "Client",
        back_populates="address",
    )

    supplier: Mapped["Supplier | None"] = relationship(
        "Supplier",
        back_populates="address"
    )