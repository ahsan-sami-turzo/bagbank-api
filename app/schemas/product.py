from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models.product import OwnershipStatus


# Product Variation Schemas
class ProductVariationBase(BaseModel):
    color_id: int
    stock_quantity: int = 0


class ProductVariationCreate(ProductVariationBase):
    pass


class ProductVariationUpdate(BaseModel):
    color_id: Optional[int] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None


class ProductVariationResponse(ProductVariationBase):
    id: int
    sku: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    color_name: Optional[str] = None
    color_hex: Optional[str] = None

    class Config:
        from_attributes = True


# Product Schemas
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    category_id: int
    material_id: int
    brand_id: int
    style_id: int
    country_id: int
    ownership_status: OwnershipStatus
    supplier_id: Optional[int] = None
    purchase_price: Optional[Decimal] = Field(None, ge=0)
    selling_price: Decimal = Field(..., ge=0)
    description: Optional[str] = None
    keywords: Optional[str] = None
    youtube_video_url: Optional[str] = Field(None, max_length=500)
    facebook_post_url: Optional[str] = Field(None, max_length=500)


class ProductCreate(ProductBase):
    variations: List[ProductVariationCreate] = []


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    category_id: Optional[int] = None
    material_id: Optional[int] = None
    brand_id: Optional[int] = None
    style_id: Optional[int] = None
    country_id: Optional[int] = None
    ownership_status: Optional[OwnershipStatus] = None
    supplier_id: Optional[int] = None
    purchase_price: Optional[Decimal] = Field(None, ge=0)
    selling_price: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = None
    keywords: Optional[str] = None
    youtube_video_url: Optional[str] = Field(None, max_length=500)
    facebook_post_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int
    slug: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    variations: List[ProductVariationResponse] = []
    
    # Related entity names for display
    category_name: Optional[str] = None
    material_name: Optional[str] = None
    brand_name: Optional[str] = None
    style_name: Optional[str] = None
    country_name: Optional[str] = None
    supplier_name: Optional[str] = None

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    id: int
    name: str
    slug: str
    selling_price: Decimal
    ownership_status: OwnershipStatus
    is_active: bool
    created_at: datetime
    category_name: Optional[str] = None
    brand_name: Optional[str] = None
    supplier_name: Optional[str] = None
    variation_count: int = 0

    class Config:
        from_attributes = True


# Product with minimal data for dropdowns
class ProductMinimalResponse(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True
