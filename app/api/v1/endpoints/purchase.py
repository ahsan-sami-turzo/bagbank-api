from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.services.purchase import purchase_service
from app.models.purchase import PurchaseStatus, PaymentStatus
from app.schemas.purchase import (
    PurchaseCreate, PurchaseUpdate, PurchaseResponse, 
    PurchaseListResponse, PaymentHistoryCreate, PaymentHistoryResponse
)
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=PurchaseResponse)
async def create_purchase(
    purchase: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new purchase"""
    return purchase_service.create_purchase(db, purchase, current_user.id)

@router.get("/", response_model=List[PurchaseListResponse])
async def get_purchases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    supplier_id: Optional[str] = None,
    status: Optional[PurchaseStatus] = None,
    payment_status: Optional[PaymentStatus] = None,
    db: Session = Depends(get_db)
):
    """Get all purchases with optional filtering"""
    return purchase_service.get_purchases(
        db, skip=skip, limit=limit,
        supplier_id=supplier_id,
        status=status,
        payment_status=payment_status
    )

@router.get("/{purchase_id}", response_model=PurchaseResponse)
async def get_purchase(
    purchase_id: str,
    db: Session = Depends(get_db)
):
    """Get a purchase by ID"""
    purchase = purchase_service.get_purchase(db, purchase_id)
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase not found"
        )
    return purchase

@router.put("/{purchase_id}/status", response_model=PurchaseResponse)
async def update_purchase_status(
    purchase_id: str,
    new_status: PurchaseStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update purchase status"""
    return purchase_service.update_purchase_status(db, purchase_id, new_status, current_user.id)

@router.post("/{purchase_id}/payments", response_model=PaymentHistoryResponse)
async def add_payment(
    purchase_id: str,
    payment: PaymentHistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a payment to a purchase"""
    return purchase_service.add_payment(db, purchase_id, payment, current_user.id)