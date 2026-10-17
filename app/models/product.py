from uuid import UUID, uuid4

from sqlalchemy import String, ForeignKey, Numeric, Integer, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from app.db.base import Base
from decimal import Decimal
from sqlalchemy import func

class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price >= 0", name="check_product_price"),
        CheckConstraint("available_stock >= 0", name="check_product_stock"),
    )

    id: Mapped[UUID] = mapped_column( 
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4)
    
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    
    category_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("categories.id"),
        nullable=False
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable=False,
    )
    
    available_stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    last_update_date: Mapped[datetime] = mapped_column(   # число последней закупки
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ) 

    supplier_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("suppliers.id"),
        nullable=False
    )

    image_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("images.id", ondelete="SET NULL"),
        nullable=True,
        unique=True
    )

    


    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
    )

    supplier: Mapped["Supplier"] = relationship(
        "Supplier",
        back_populates="products",
    )

    image: Mapped["Image | None"] = relationship(
        "Image",
        back_populates="product",
    )

