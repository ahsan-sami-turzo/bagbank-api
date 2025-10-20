from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from typing import List, Optional
from decimal import Decimal
from app.models.return_workflow import PurchaseReturn, RefundStatus
from app.models.stock import ChangeType
from app.schemas.purchase_return import PurchaseReturnCreate, PurchaseReturnUpdate
from app.services.stock import stock_service


class PurchaseReturnService:
    def create_purchase_return(
        self,
        db: Session,
        return_data: PurchaseReturnCreate,
        user_id: str
    ) -> PurchaseReturn:
        """Create a new purchase return and update stock"""
        
        # Create return record
        db_obj = PurchaseReturn(
            **return_data.dict(),
            created_by=user_id
        )
        db.add(db_obj)
        db.flush()
        
        # Update stock
        stock_service.create_stock_entry(
            db=db,
            product_variation_id=return_data.product_variation_id,
            change_type=ChangeType.RETURN,
            quantity_change=return_data.quantity_returned,
            source_type="PurchaseReturn",
            source_id=db_obj.id,
            user_id=user_id,
            notes=f"Purchase return: {return_data.reason if return_data.reason else 'No reason provided'}"
        )
        
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_purchase_return(self, db: Session, return_id: str) -> Optional[PurchaseReturn]:
        """Get a purchase return by ID"""
        return db.query(PurchaseReturn).options(
            joinedload(PurchaseReturn.product_variation),
            joinedload(PurchaseReturn.creator)
        ).filter(PurchaseReturn.id == return_id).first()
    
    def get_purchase_returns(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        refund_status: Optional[RefundStatus] = None
    ) -> List[PurchaseReturn]:
        """Get purchase returns with optional filtering"""
        query = db.query(PurchaseReturn).options(
            joinedload(PurchaseReturn.product_variation),
            joinedload(PurchaseReturn.creator)
        )
        
        if refund_status:
            query = query.filter(PurchaseReturn.refund_status == refund_status)
        
        return query.offset(skip).limit(limit).all()
    
    def update_purchase_return(
        self,
        db: Session,
        db_obj: PurchaseReturn,
        obj_in: PurchaseReturnUpdate
    ) -> PurchaseReturn:
        """Update a purchase return"""
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if value is not None:
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


return_service = PurchaseReturnService()