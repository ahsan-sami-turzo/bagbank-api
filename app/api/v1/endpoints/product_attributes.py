from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.product_attributes import (
    category_service, material_service, style_service,
    brand_service, color_service, country_service
)
from app.schemas.product_attributes import (
    ProductCategoryCreate, ProductCategoryUpdate, ProductCategoryResponse,
    ProductMaterialCreate, ProductMaterialUpdate, ProductMaterialResponse,
    ProductStyleCreate, ProductStyleUpdate, ProductStyleResponse,
    ProductBrandCreate, ProductBrandUpdate, ProductBrandResponse,
    ProductColorCreate, ProductColorUpdate, ProductColorResponse,
    CountryOfOriginCreate, CountryOfOriginUpdate, CountryOfOriginResponse
)

router = APIRouter()


# Category endpoints
@router.post("/categories", response_model=ProductCategoryResponse)
async def create_category(
    category: ProductCategoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new product category"""
    return category_service.create(db, category.dict())


@router.get("/categories", response_model=List[ProductCategoryResponse])
async def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all product categories"""
    return category_service.get_multi(db, skip=skip, limit=limit, is_active=is_active)


@router.get("/categories/{category_id}", response_model=ProductCategoryResponse)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Get a product category by ID"""
    category = category_service.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.put("/categories/{category_id}", response_model=ProductCategoryResponse)
async def update_category(
    category_id: int,
    category_update: ProductCategoryUpdate,
    db: Session = Depends(get_db)
):
    """Update a product category"""
    category = category_service.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category_service.update(db, category, category_update.dict(exclude_unset=True))


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product category"""
    category = category_service.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    category_service.delete(db, category_id)
    return {"message": "Category deleted successfully"}


# Material endpoints
@router.post("/materials", response_model=ProductMaterialResponse)
async def create_material(
    material: ProductMaterialCreate,
    db: Session = Depends(get_db)
):
    """Create a new product material"""
    return material_service.create(db, material.dict())


@router.get("/materials", response_model=List[ProductMaterialResponse])
async def get_materials(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all product materials"""
    return material_service.get_multi(db, skip=skip, limit=limit, is_active=is_active)


@router.get("/materials/{material_id}", response_model=ProductMaterialResponse)
async def get_material(
    material_id: int,
    db: Session = Depends(get_db)
):
    """Get a product material by ID"""
    material = material_service.get(db, material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    return material


@router.put("/materials/{material_id}", response_model=ProductMaterialResponse)
async def update_material(
    material_id: int,
    material_update: ProductMaterialUpdate,
    db: Session = Depends(get_db)
):
    """Update a product material"""
    material = material_service.get(db, material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    return material_service.update(db, material, material_update.dict(exclude_unset=True))


@router.delete("/materials/{material_id}")
async def delete_material(
    material_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product material"""
    material = material_service.get(db, material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    material_service.delete(db, material_id)
    return {"message": "Material deleted successfully"}


# Style endpoints
@router.post("/styles", response_model=ProductStyleResponse)
async def create_style(
    style: ProductStyleCreate,
    db: Session = Depends(get_db)
):
    """Create a new product style"""
    return style_service.create(db, style.dict())


@router.get("/styles", response_model=List[ProductStyleResponse])
async def get_styles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all product styles"""
    return style_service.get_multi(db, skip=skip, limit=limit, is_active=is_active)


@router.get("/styles/{style_id}", response_model=ProductStyleResponse)
async def get_style(
    style_id: int,
    db: Session = Depends(get_db)
):
    """Get a product style by ID"""
    style = style_service.get(db, style_id)
    if not style:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Style not found"
        )
    return style


@router.put("/styles/{style_id}", response_model=ProductStyleResponse)
async def update_style(
    style_id: int,
    style_update: ProductStyleUpdate,
    db: Session = Depends(get_db)
):
    """Update a product style"""
    style = style_service.get(db, style_id)
    if not style:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Style not found"
        )
    return style_service.update(db, style, style_update.dict(exclude_unset=True))


@router.delete("/styles/{style_id}")
async def delete_style(
    style_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product style"""
    style = style_service.get(db, style_id)
    if not style:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Style not found"
        )
    style_service.delete(db, style_id)
    return {"message": "Style deleted successfully"}


# Brand endpoints
@router.post("/brands", response_model=ProductBrandResponse)
async def create_brand(
    brand: ProductBrandCreate,
    db: Session = Depends(get_db)
):
    """Create a new product brand"""
    return brand_service.create(db, brand.dict())


@router.get("/brands", response_model=List[ProductBrandResponse])
async def get_brands(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all product brands"""
    return brand_service.get_multi(db, skip=skip, limit=limit, is_active=is_active)


@router.get("/brands/{brand_id}", response_model=ProductBrandResponse)
async def get_brand(
    brand_id: int,
    db: Session = Depends(get_db)
):
    """Get a product brand by ID"""
    brand = brand_service.get(db, brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found"
        )
    return brand


@router.put("/brands/{brand_id}", response_model=ProductBrandResponse)
async def update_brand(
    brand_id: int,
    brand_update: ProductBrandUpdate,
    db: Session = Depends(get_db)
):
    """Update a product brand"""
    brand = brand_service.get(db, brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found"
        )
    return brand_service.update(db, brand, brand_update.dict(exclude_unset=True))


@router.delete("/brands/{brand_id}")
async def delete_brand(
    brand_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product brand"""
    brand = brand_service.get(db, brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found"
        )
    brand_service.delete(db, brand_id)
    return {"message": "Brand deleted successfully"}


# Color endpoints
@router.post("/colors", response_model=ProductColorResponse)
async def create_color(
    color: ProductColorCreate,
    db: Session = Depends(get_db)
):
    """Create a new product color"""
    return color_service.create(db, color.dict())


@router.get("/colors", response_model=List[ProductColorResponse])
async def get_colors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all product colors"""
    return color_service.get_multi(db, skip=skip, limit=limit, is_active=is_active)


@router.get("/colors/{color_id}", response_model=ProductColorResponse)
async def get_color(
    color_id: int,
    db: Session = Depends(get_db)
):
    """Get a product color by ID"""
    color = color_service.get(db, color_id)
    if not color:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found"
        )
    return color


@router.put("/colors/{color_id}", response_model=ProductColorResponse)
async def update_color(
    color_id: int,
    color_update: ProductColorUpdate,
    db: Session = Depends(get_db)
):
    """Update a product color"""
    color = color_service.get(db, color_id)
    if not color:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found"
        )
    return color_service.update(db, color, color_update.dict(exclude_unset=True))


@router.delete("/colors/{color_id}")
async def delete_color(
    color_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product color"""
    color = color_service.get(db, color_id)
    if not color:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found"
        )
    color_service.delete(db, color_id)
    return {"message": "Color deleted successfully"}


# Country endpoints
@router.post("/countries", response_model=CountryOfOriginResponse)
async def create_country(
    country: CountryOfOriginCreate,
    db: Session = Depends(get_db)
):
    """Create a new country of origin"""
    return country_service.create(db, country.dict())


@router.get("/countries", response_model=List[CountryOfOriginResponse])
async def get_countries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all countries of origin"""
    return country_service.get_multi(db, skip=skip, limit=limit, is_active=is_active)


@router.get("/countries/{country_id}", response_model=CountryOfOriginResponse)
async def get_country(
    country_id: int,
    db: Session = Depends(get_db)
):
    """Get a country of origin by ID"""
    country = country_service.get(db, country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    return country


@router.put("/countries/{country_id}", response_model=CountryOfOriginResponse)
async def update_country(
    country_id: int,
    country_update: CountryOfOriginUpdate,
    db: Session = Depends(get_db)
):
    """Update a country of origin"""
    country = country_service.get(db, country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    return country_service.update(db, country, country_update.dict(exclude_unset=True))


@router.delete("/countries/{country_id}")
async def delete_country(
    country_id: int,
    db: Session = Depends(get_db)
):
    """Delete a country of origin"""
    country = country_service.get(db, country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    country_service.delete(db, country_id)
    return {"message": "Country deleted successfully"}
