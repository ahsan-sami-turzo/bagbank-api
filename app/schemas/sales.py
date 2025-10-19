from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models.sales import SalesOrderStatus, SalesPaymentStatus


# Sales Detail Schemas
class SalesDetailBase(BaseModel):
    product_variation_id: str
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., gt=0)


class SalesDetailCreate(SalesDetailBase):
    pass


class SalesDetailUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    unit_price: Optional[Decimal] = Field(None, gt=0)


class SalesDetailResponse(SalesDetailBase):
    id: str
    sales_order_id: str
    subtotal: Decimal
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Sales Order Schemas
class SalesOrderBase(BaseModel):
    customer_name: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None


class SalesOrderCreate(SalesOrderBase):
    details: List[SalesDetailCreate] = []


class SalesOrderUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, max_length=200)
    status: Optional[SalesOrderStatus] = None
    payment_status: Optional[SalesPaymentStatus] = None
    notes: Optional[str] = None


class SalesOrderResponse(SalesOrderBase):
    id: str
    order_date: datetime
    status: SalesOrderStatus
    payment_status: SalesPaymentStatus
    total_price: Decimal
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: str
    details: List[SalesDetailResponse] = []
    
    # Related entity names for display
    creator_name: Optional[str] = None

    class Config:
        from_attributes = True


class SalesOrderListResponse(BaseModel):
    id: str
    customer_name: Optional[str]
    status: SalesOrderStatus
    payment_status: SalesPaymentStatus
    total_price: Decimal
    order_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
