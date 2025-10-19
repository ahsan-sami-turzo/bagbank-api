from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Base schemas for product attributes
class ProductAttributeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True


class ProductAttributeCreate(ProductAttributeBase):
    pass


class ProductAttributeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None


class ProductAttributeResponse(ProductAttributeBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Category schemas
class ProductCategoryCreate(ProductAttributeCreate):
    pass


class ProductCategoryUpdate(ProductAttributeUpdate):
    pass


class ProductCategoryResponse(ProductAttributeResponse):
    pass


# Material schemas
class ProductMaterialCreate(ProductAttributeCreate):
    pass


class ProductMaterialUpdate(ProductAttributeUpdate):
    pass


class ProductMaterialResponse(ProductAttributeResponse):
    pass


# Style schemas
class ProductStyleCreate(ProductAttributeCreate):
    pass


class ProductStyleUpdate(ProductAttributeUpdate):
    pass


class ProductStyleResponse(ProductAttributeResponse):
    pass


# Brand schemas
class ProductBrandCreate(ProductAttributeCreate):
    pass


class ProductBrandUpdate(ProductAttributeUpdate):
    pass


class ProductBrandResponse(ProductAttributeResponse):
    pass


# Color schemas
class ProductColorCreate(ProductAttributeCreate):
    hex_code: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    rgb_code: Optional[str] = Field(None, pattern=r'^rgb\(\d{1,3},\s*\d{1,3},\s*\d{1,3}\)$')


class ProductColorUpdate(ProductAttributeUpdate):
    hex_code: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    rgb_code: Optional[str] = Field(None, pattern=r'^rgb\(\d{1,3},\s*\d{1,3},\s*\d{1,3}\)$')


class ProductColorResponse(ProductAttributeResponse):
    hex_code: Optional[str] = None
    rgb_code: Optional[str] = None


# Country schemas
class CountryOfOriginCreate(ProductAttributeCreate):
    pass


class CountryOfOriginUpdate(ProductAttributeUpdate):
    pass


class CountryOfOriginResponse(ProductAttributeResponse):
    pass
