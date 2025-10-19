from sqlalchemy import Column, String, DateTime, Integer, Numeric, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum
import uuid


class SalesOrderStatus(str, enum.Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"


class SalesPaymentStatus(str, enum.Enum):
    UNPAID = "unpaid"
    PARTIALLY_PAID = "partially_paid"
    FULLY_PAID = "fully_paid"


class SalesOrder(Base):
    __tablename__ = "sales_orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    order_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    customer_name = Column(String(200), nullable=True)
    status = Column(Enum(SalesOrderStatus), nullable=False, default=SalesOrderStatus.DRAFT)
    payment_status = Column(Enum(SalesPaymentStatus), nullable=False, default=SalesPaymentStatus.UNPAID)
    total_price = Column(Numeric(12, 2), nullable=False, default=0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    details = relationship("SalesDetail", back_populates="sales_order", cascade="all, delete-orphan")
    creator = relationship("User", back_populates="created_sales_orders")

    def __repr__(self):
        return f"<SalesOrder(id={self.id}, customer_name='{self.customer_name}', status='{self.status}')>"


class SalesDetail(Base):
    __tablename__ = "sales_details"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    sales_order_id = Column(String, ForeignKey("sales_orders.id"), nullable=False)
    product_variation_id = Column(Integer, ForeignKey("product_variations.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    sales_order = relationship("SalesOrder", back_populates="details")
    product_variation = relationship("ProductVariation", back_populates="sales_details")

    def __repr__(self):
        return f"<SalesDetail(id={self.id}, sales_order_id={self.sales_order_id}, quantity={self.quantity})>"
