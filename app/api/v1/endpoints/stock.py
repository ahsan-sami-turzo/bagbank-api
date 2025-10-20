from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.stock import stock_service
from app.schemas.stock import (
    StockLedgerResponse, InventoryCountCreate,
    InventoryCountResponse, InventoryCountListResponse,
    StockSummaryResponse
)
from app.models.stock import ChangeType
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/ledger", response_model=List[StockLedgerResponse])
async def get_stock_ledger(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    product_variation_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get stock ledger entries"""
    return stock_service.get_stock_ledger(
        db, product_variation_id=product_variation_id,
        skip=skip, limit=limit
    )

@router.get("/summary", response_model=List[StockSummaryResponse])
async def get_stock_summary(
    low_stock_threshold: int = Query(10, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get stock summary for all product variations"""
    return stock_service.get_stock_summary(
        db, low_stock_threshold=low_stock_threshold,
        skip=skip, limit=limit
    )

@router.get("/low-stock", response_model=List[StockSummaryResponse])
async def get_low_stock_items(
    threshold: int = Query(10, ge=0),
    db: Session = Depends(get_db)
):
    """Get items with stock below threshold"""
    return stock_service.get_low_stock_items(db, threshold=threshold)

@router.post("/count", response_model=InventoryCountResponse)
async def create_inventory_count(
    count_data: InventoryCountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create an inventory count"""
    return stock_service.create_inventory_count(
        db,
        product_variation_id=count_data.product_variation_id,
        counted_quantity=count_data.counted_quantity,
        operator_id=current_user.id,
        notes=count_data.notes
    )

@router.get("/count", response_model=List[InventoryCountListResponse])
async def get_inventory_counts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    product_variation_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get inventory count records"""
    return stock_service.get_inventory_counts(
        db,
        product_variation_id=product_variation_id,
        skip=skip,
        limit=limit
    )