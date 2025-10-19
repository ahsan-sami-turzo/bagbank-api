from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.product import product_service
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, 
    ProductListResponse, ProductMinimalResponse
)
from app.models.product import OwnershipStatus

router = APIRouter()


@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new product with variations"""
    return product_service.create(db, product)


@router.get("/", response_model=List[ProductListResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category_id: Optional[int] = None,
    brand_id: Optional[int] = None,
    ownership_status: Optional[OwnershipStatus] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all products with optional filtering"""
    products = product_service.get_multi(
        db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        brand_id=brand_id,
        ownership_status=ownership_status,
        is_active=is_active,
        search=search
    )
    
    # Add variation count and related names
    result = []
    for product in products:
        product_dict = {
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "selling_price": product.selling_price,
            "ownership_status": product.ownership_status,
            "is_active": product.is_active,
            "created_at": product.created_at,
            "category_name": product.category.name if product.category else None,
            "brand_name": product.brand.name if product.brand else None,
            "supplier_name": product.supplier.name if product.supplier else None,
            "variation_count": len(product.variations) if hasattr(product, 'variations') else 0
        }
        result.append(ProductListResponse(**product_dict))
    
    return result


@router.get("/minimal", response_model=List[ProductMinimalResponse])
async def get_products_minimal(
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """Get products with minimal data for dropdowns"""
    products = product_service.get_multi(db, is_active=is_active)
    return [ProductMinimalResponse(
        id=p.id,
        name=p.name,
        slug=p.slug
    ) for p in products]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get a product by ID with all relationships"""
    product = product_service.get(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Add related entity names
    product_dict = product.__dict__.copy()
    product_dict.update({
        "category_name": product.category.name if product.category else None,
        "material_name": product.material.name if product.material else None,
        "brand_name": product.brand.name if product.brand else None,
        "style_name": product.style.name if product.style else None,
        "country_name": product.country.name if product.country else None,
        "supplier_name": product.supplier.name if product.supplier else None,
    })
    
    # Add color names and hex codes to variations
    variations = []
    for variation in product.variations:
        var_dict = variation.__dict__.copy()
        var_dict.update({
            "color_name": variation.color.name if variation.color else None,
            "color_hex": variation.color.hex_code if variation.color else None
        })
        variations.append(var_dict)
    
    product_dict["variations"] = variations
    
    return ProductResponse(**product_dict)


@router.get("/slug/{slug}", response_model=ProductResponse)
async def get_product_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get a product by slug with all relationships"""
    product = product_service.get_by_slug(db, slug)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Add related entity names
    product_dict = product.__dict__.copy()
    product_dict.update({
        "category_name": product.category.name if product.category else None,
        "material_name": product.material.name if product.material else None,
        "brand_name": product.brand.name if product.brand else None,
        "style_name": product.style.name if product.style else None,
        "country_name": product.country.name if product.country else None,
        "supplier_name": product.supplier.name if product.supplier else None,
    })
    
    # Add color names and hex codes to variations
    variations = []
    for variation in product.variations:
        var_dict = variation.__dict__.copy()
        var_dict.update({
            "color_name": variation.color.name if variation.color else None,
            "color_hex": variation.color.hex_code if variation.color else None
        })
        variations.append(var_dict)
    
    product_dict["variations"] = variations
    
    return ProductResponse(**product_dict)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product"""
    product = product_service.get(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product_service.update(db, product, product_update)


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product"""
    product = product_service.get(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    product_service.delete(db, product_id)
    return {"message": "Product deleted successfully"}


@router.get("/suppliers/{ownership_status}", response_model=List)
async def get_suppliers_by_ownership(
    ownership_status: OwnershipStatus,
    db: Session = Depends(get_db)
):
    """Get suppliers based on product ownership status"""
    return product_service.get_suppliers_by_ownership(db, ownership_status)
