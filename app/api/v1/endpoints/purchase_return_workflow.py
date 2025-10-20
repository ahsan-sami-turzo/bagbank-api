from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.purchase_return import return_service
from app.schemas.purchase_return import (
    PurchaseReturnCreate, PurchaseReturnUpdate, 
    PurchaseReturnResponse, PurchaseReturnListResponse
)
from app.models.return_workflow import RefundStatus
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=PurchaseReturnResponse)
async def create_purchase_return(
    purchase_return_data: PurchaseReturnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new purchase return"""
    return return_service.create_purchase_return(
        db, purchase_return_data, current_user.id
    )

@router.get("/", response_model=List[PurchaseReturnListResponse])
async def get_purchase_returns(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    refund_status: Optional[RefundStatus] = None,
    db: Session = Depends(get_db)
):
    """Get all purchase returns with optional filtering"""
    return return_service.get_purchase_returns(
        db, skip=skip, limit=limit,
        refund_status=refund_status
    )

@router.get("/{purchase_return_id}", response_model=PurchaseReturnResponse)
async def get_purchase_return(
    purchase_return_id: str,
    db: Session = Depends(get_db)
):
    """Get a purchase return by ID"""
    purchase_return = return_service.get_purchase_return(db, purchase_return_id)
    if not purchase_return:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase return not found"
        )
    return purchase_return

@router.put("/{purchase_return_id}", response_model=PurchaseReturnResponse)
async def update_purchase_return(
    purchase_return_id: str,
    purchase_return_update: PurchaseReturnUpdate,
    db: Session = Depends(get_db)
):
    """Update a purchase return"""
    purchase_return = return_service.get_purchase_return(db, purchase_return_id)
    if not purchase_return:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase return not found"
        )
    return return_service.update_purchase_return(
        db, purchase_return, purchase_return_update
    )