from uuid import UUID, uuid4

from sqlalchemy import String, Date, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date, datetime
from app.db.base import Base



class Client(Base):
    __tablename__ = "clients"

    id: Mapped[UUID] = mapped_column( 
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4)
    
    client_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    client_surname: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    birthday: Mapped[date] = mapped_column(Date)

    gender: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )

    registration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    address_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("addresses.id"),
        nullable=False,
        unique=True
    )


    address: Mapped["Address"] = relationship(
        "Address",
        back_populates="client",
    )