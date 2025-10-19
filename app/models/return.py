from sqlalchemy import Column, String, DateTime, Integer, Numeric, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum
import uuid


class RefundStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class PurchaseReturn(Base):
    __tablename__ = "purchase_returns"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    purchase_detail_id = Column(String, ForeignKey("purchase_details.id"), nullable=False)
    product_variation_id = Column(String, ForeignKey("product_variations.id"), nullable=False)
    quantity_returned = Column(Integer, nullable=False)
    return_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    reason = Column(Text, nullable=True)
    refund_amount = Column(Numeric(12, 2), nullable=True)
    refund_status = Column(Enum(RefundStatus), nullable=False, default=RefundStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String, ForeignKey("users.id"), nullable=False)

    # Relationships
    purchase_detail = relationship("PurchaseDetail", back_populates="returns")
    product_variation = relationship("ProductVariation", back_populates="purchase_returns")
    creator = relationship("User", back_populates="created_returns")

    def __repr__(self):
        return f"<PurchaseReturn(id={self.id}, quantity_returned={self.quantity_returned})>"
