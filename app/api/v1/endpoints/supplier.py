from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.supplier import supplier_service
from app.schemas.supplier import (
    SupplierCreate, SupplierUpdate, SupplierResponse, SupplierListResponse
)
from app.models.supplier import SupplierType

router = APIRouter()


@router.post("/", response_model=SupplierResponse)
async def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db)
):
    """Create a new supplier"""
    return supplier_service.create(db, supplier)


@router.get("/", response_model=List[SupplierResponse])
async def get_suppliers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    supplier_type: Optional[SupplierType] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all suppliers with optional filtering"""
    return supplier_service.get_multi(
        db, 
        skip=skip, 
        limit=limit, 
        supplier_type=supplier_type,
        is_active=is_active
    )


@router.get("/list", response_model=List[SupplierListResponse])
async def get_suppliers_list(
    supplier_type: Optional[SupplierType] = None,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """Get suppliers list for dropdowns"""
    return supplier_service.get_by_type(db, supplier_type, is_active) if supplier_type else supplier_service.get_multi(db, is_active=is_active)


@router.get("/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    """Get a supplier by ID"""
    supplier = supplier_service.get(db, supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    return supplier


@router.put("/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(
    supplier_id: int,
    supplier_update: SupplierUpdate,
    db: Session = Depends(get_db)
):
    """Update a supplier"""
    supplier = supplier_service.get(db, supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    return supplier_service.update(db, supplier, supplier_update)


@router.delete("/{supplier_id}")
async def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    """Delete a supplier"""
    supplier = supplier_service.get(db, supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    supplier_service.delete(db, supplier_id)
    return {"message": "Supplier deleted successfully"}


@router.get("/type/{supplier_type}", response_model=List[SupplierListResponse])
async def get_suppliers_by_type(
    supplier_type: SupplierType,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """Get suppliers by type (for product forms)"""
    return supplier_service.get_by_type(db, supplier_type, is_active)
