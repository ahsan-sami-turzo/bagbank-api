from sqlalchemy import Column, String, DateTime, Integer, Numeric, Text, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum
import uuid


class PurchaseStatus(str, enum.Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    RECEIVED = "received"
    PARTIALLY_RECEIVED = "partially_received"


class PaymentStatus(str, enum.Enum):
    UNPAID = "unpaid"
    PARTIALLY_PAID = "partially_paid"
    FULLY_PAID = "fully_paid"


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    purchase_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    status = Column(Enum(PurchaseStatus), nullable=False, default=PurchaseStatus.DRAFT)
    payment_status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.UNPAID)
    expected_arrival_date = Column(Date, nullable=True)
    supplier_reference = Column(String(100), nullable=True)
    total_price = Column(Numeric(12, 2), nullable=False, default=0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    supplier = relationship("Supplier", back_populates="purchases")
    details = relationship("PurchaseDetail", back_populates="purchase", cascade="all, delete-orphan")
    payments = relationship("PaymentHistory", back_populates="purchase", cascade="all, delete-orphan")
    creator = relationship("User", back_populates="created_purchases")

    def __repr__(self):
        return f"<Purchase(id={self.id}, supplier_id={self.supplier_id}, status='{self.status}')>"


class PurchaseDetail(Base):
    __tablename__ = "purchase_details"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    purchase_id = Column(String, ForeignKey("purchases.id"), nullable=False)
    product_variation_id = Column(Integer, ForeignKey("product_variations.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    purchase = relationship("Purchase", back_populates="details")
    product_variation = relationship("ProductVariation", back_populates="purchase_details")
    returns = relationship("PurchaseReturn", back_populates="purchase_detail", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PurchaseDetail(id={self.id}, purchase_id={self.purchase_id}, quantity={self.quantity})>"


class PaymentHistory(Base):
    __tablename__ = "payment_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    purchase_id = Column(String, ForeignKey("purchases.id"), nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    amount_paid = Column(Numeric(12, 2), nullable=False)
    payment_method = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    purchase = relationship("Purchase", back_populates="payments")
    creator = relationship("User", back_populates="created_payments")

    def __repr__(self):
        return f"<PaymentHistory(id={self.id}, purchase_id={self.purchase_id}, amount={self.amount_paid})>"
