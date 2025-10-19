from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from app.models.supplier import SupplierType


class SupplierBase(BaseModel):
    supplier_type: SupplierType
    name: str = Field(..., min_length=1, max_length=200)
    address: Optional[str] = Field(None, max_length=500)
    contact_person: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    whatsapp_number: Optional[str] = Field(None, max_length=20)
    email_address: Optional[EmailStr] = None
    facebook_profile_url: Optional[str] = Field(None, max_length=500)


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    supplier_type: Optional[SupplierType] = None
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    address: Optional[str] = Field(None, max_length=500)
    contact_person: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    whatsapp_number: Optional[str] = Field(None, max_length=20)
    email_address: Optional[EmailStr] = None
    facebook_profile_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class SupplierResponse(SupplierBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SupplierListResponse(BaseModel):
    id: int
    name: str
    supplier_type: SupplierType
    contact_person: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True
