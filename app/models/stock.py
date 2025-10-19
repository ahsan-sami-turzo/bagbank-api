from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum
import uuid


class ChangeType(str, enum.Enum):
    PURCHASE = "purchase"
    RETURN = "return"
    SALE = "sale"
    ADJUSTMENT = "adjustment"
    INVENTORY_COUNT = "inventory_count"


class StockLedger(Base):
    __tablename__ = "stock_ledger"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    product_variation_id = Column(Integer, ForeignKey("product_variations.id"), nullable=False)
    change_type = Column(Enum(ChangeType), nullable=False)
    source_type = Column(String(50), nullable=True)  # e.g., "PurchaseDetail", "SalesDetail"
    source_id = Column(String, nullable=True)  # UUID of the source document
    quantity_change = Column(Integer, nullable=False)
    running_balance = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    notes = Column(Text, nullable=True)

    # Relationships
    product_variation = relationship("ProductVariation", back_populates="stock_ledger_entries")
    user = relationship("User", back_populates="stock_ledger_entries")

    def __repr__(self):
        return f"<StockLedger(id={self.id}, change_type='{self.change_type}', quantity_change={self.quantity_change})>"


class InventoryCount(Base):
    __tablename__ = "inventory_counts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    product_variation_id = Column(Integer, ForeignKey("product_variations.id"), nullable=False)
    counted_quantity = Column(Integer, nullable=False)
    system_stock = Column(Integer, nullable=False)  # Stock at time of count
    count_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    difference = Column(Integer, nullable=False)  # counted_quantity - system_stock
    adjustment_entry_id = Column(String, ForeignKey("stock_ledger.id"), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    product_variation = relationship("ProductVariation", back_populates="inventory_counts")
    adjustment_entry = relationship("StockLedger", foreign_keys=[adjustment_entry_id])
    operator = relationship("User", back_populates="inventory_counts")

    def __repr__(self):
        return f"<InventoryCount(id={self.id}, counted_quantity={self.counted_quantity}, difference={self.difference})>"
