from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class UserRole(str, enum.Enum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    MODERATOR = "moderator"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships for inventory management
    created_purchases = relationship("Purchase", back_populates="creator")
    created_payments = relationship("PaymentHistory", back_populates="creator")
    created_returns = relationship("PurchaseReturn", back_populates="creator")
    created_sales_orders = relationship("SalesOrder", back_populates="creator")
    stock_ledger_entries = relationship("StockLedger", back_populates="user")
    inventory_counts = relationship("InventoryCount", back_populates="operator")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"

