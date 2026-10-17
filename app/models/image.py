from uuid import UUID, uuid4
from sqlalchemy import LargeBinary
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base



class Image(Base):
    __tablename__ = "images"

    id: Mapped[UUID] = mapped_column( 
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    image: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False
    )

    product: Mapped["Product | None"] = relationship(
    "Product",
    back_populates="image",
)