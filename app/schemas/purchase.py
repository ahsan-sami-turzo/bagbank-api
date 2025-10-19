from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from app.models.purchase import PurchaseStatus, PaymentStatus


# Purchase Detail Schemas
class PurchaseDetailBase(BaseModel):
    product_variation_id: str
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., gt=0)


class PurchaseDetailCreate(PurchaseDetailBase):
    pass


class PurchaseDetailUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    unit_price: Optional[Decimal] = Field(None, gt=0)


class PurchaseDetailResponse(PurchaseDetailBase):
    id: str
    purchase_id: str
    subtotal: Decimal
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Payment History Schemas
class PaymentHistoryBase(BaseModel):
    amount_paid: Decimal = Field(..., gt=0)
    payment_method: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None


class PaymentHistoryCreate(PaymentHistoryBase):
    pass


class PaymentHistoryResponse(PaymentHistoryBase):
    id: str
    purchase_id: str
    payment_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# Purchase Schemas
class PurchaseBase(BaseModel):
    supplier_id: str
    purchase_date: Optional[datetime] = None
    expected_arrival_date: Optional[date] = None
    supplier_reference: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class PurchaseCreate(PurchaseBase):
    details: List[PurchaseDetailCreate] = []


class PurchaseUpdate(BaseModel):
    status: Optional[PurchaseStatus] = None
    expected_arrival_date: Optional[date] = None
    supplier_reference: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class PurchaseResponse(PurchaseBase):
    id: str
    status: PurchaseStatus
    payment_status: PaymentStatus
    total_price: Decimal
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: str
    details: List[PurchaseDetailResponse] = []
    payments: List[PaymentHistoryResponse] = []
    
    # Related entity names for display
    supplier_name: Optional[str] = None
    creator_name: Optional[str] = None

    class Config:
        from_attributes = True


class PurchaseListResponse(BaseModel):
    id: str
    supplier_name: str
    status: PurchaseStatus
    payment_status: PaymentStatus
    total_price: Decimal
    purchase_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
