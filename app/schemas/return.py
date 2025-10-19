from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.return import RefundStatus


class PurchaseReturnBase(BaseModel):
    purchase_detail_id: str
    product_variation_id: str
    quantity_returned: int = Field(..., gt=0)
    reason: Optional[str] = None
    refund_amount: Optional[Decimal] = Field(None, ge=0)
    refund_status: RefundStatus = RefundStatus.PENDING


class PurchaseReturnCreate(PurchaseReturnBase):
    pass


class PurchaseReturnUpdate(BaseModel):
    quantity_returned: Optional[int] = Field(None, gt=0)
    reason: Optional[str] = None
    refund_amount: Optional[Decimal] = Field(None, ge=0)
    refund_status: Optional[RefundStatus] = None


class PurchaseReturnResponse(PurchaseReturnBase):
    id: str
    return_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: str
    
    # Related entity names for display
    product_name: Optional[str] = None
    color_name: Optional[str] = None
    sku: Optional[str] = None
    creator_name: Optional[str] = None

    class Config:
        from_attributes = True


class PurchaseReturnListResponse(BaseModel):
    id: str
    product_name: str
    color_name: str
    sku: str
    quantity_returned: int
    refund_amount: Optional[Decimal]
    refund_status: RefundStatus
    return_date: datetime

    class Config:
        from_attributes = True
