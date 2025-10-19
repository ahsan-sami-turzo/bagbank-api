from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.stock import ChangeType


# Stock Ledger Schemas
class StockLedgerBase(BaseModel):
    product_variation_id: str
    change_type: ChangeType
    source_type: Optional[str] = Field(None, max_length=50)
    source_id: Optional[str] = None
    quantity_change: int
    notes: Optional[str] = None


class StockLedgerCreate(StockLedgerBase):
    pass


class StockLedgerResponse(StockLedgerBase):
    id: str
    running_balance: int
    timestamp: datetime
    user_id: str
    
    # Related entity names for display
    product_name: Optional[str] = None
    color_name: Optional[str] = None
    sku: Optional[str] = None
    user_name: Optional[str] = None

    class Config:
        from_attributes = True


# Inventory Count Schemas
class InventoryCountBase(BaseModel):
    product_variation_id: str
    counted_quantity: int = Field(..., ge=0)
    notes: Optional[str] = None


class InventoryCountCreate(InventoryCountBase):
    pass


class InventoryCountUpdate(BaseModel):
    counted_quantity: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None


class InventoryCountResponse(InventoryCountBase):
    id: str
    system_stock: int
    count_date: datetime
    difference: int
    adjustment_entry_id: Optional[str]
    created_at: datetime
    operator_id: str
    
    # Related entity names for display
    product_name: Optional[str] = None
    color_name: Optional[str] = None
    sku: Optional[str] = None
    operator_name: Optional[str] = None

    class Config:
        from_attributes = True


class InventoryCountListResponse(BaseModel):
    id: str
    product_name: str
    color_name: str
    sku: str
    system_stock: int
    counted_quantity: int
    difference: int
    count_date: datetime

    class Config:
        from_attributes = True


# Stock Summary Schemas
class StockSummaryResponse(BaseModel):
    product_variation_id: str
    product_name: str
    color_name: str
    sku: str
    current_stock: int
    selling_price: float
    purchase_price: Optional[float]
    total_value: float  # current_stock * selling_price
    is_low_stock: bool

    class Config:
        from_attributes = True
