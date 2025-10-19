from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc
from typing import List, Optional
from decimal import Decimal
from app.models.purchase import Purchase, PurchaseDetail, PaymentHistory, PurchaseStatus, PaymentStatus
from app.schemas.purchase import PurchaseCreate, PurchaseUpdate, PaymentHistoryCreate
from app.services.stock import stock_service
from app.models.stock import ChangeType


class PurchaseService:
    def create_purchase(
        self,
        db: Session,
        purchase_data: PurchaseCreate,
        user_id: str
    ) -> Purchase:
        """Create a new purchase with details"""
        
        # Calculate total price
        total_price = sum(
            detail.quantity * detail.unit_price 
            for detail in purchase_data.details
        )
        
        # Create purchase
        purchase = Purchase(
            supplier_id=purchase_data.supplier_id,
            purchase_date=purchase_data.purchase_date,
            expected_arrival_date=purchase_data.expected_arrival_date,
            supplier_reference=purchase_data.supplier_reference,
            notes=purchase_data.notes,
            total_price=total_price,
            created_by=user_id
        )
        
        db.add(purchase)
        db.flush()  # Get purchase ID
        
        # Create purchase details
        for detail_data in purchase_data.details:
            subtotal = detail_data.quantity * detail_data.unit_price
            
            detail = PurchaseDetail(
                purchase_id=purchase.id,
                product_variation_id=detail_data.product_variation_id,
                quantity=detail_data.quantity,
                unit_price=detail_data.unit_price,
                subtotal=subtotal
            )
            
            db.add(detail)
        
        db.commit()
        db.refresh(purchase)
        
        return purchase
    
    def update_purchase_status(
        self,
        db: Session,
        purchase_id: str,
        new_status: PurchaseStatus,
        user_id: str
    ) -> Purchase:
        """Update purchase status and handle stock changes"""
        
        purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
        if not purchase:
            raise ValueError(f"Purchase {purchase_id} not found")
        
        old_status = purchase.status
        purchase.status = new_status
        
        # If status changed to RECEIVED, update stock
        if old_status != PurchaseStatus.RECEIVED and new_status == PurchaseStatus.RECEIVED:
            for detail in purchase.details:
                stock_service.create_stock_entry(
                    db=db,
                    product_variation_id=detail.product_variation_id,
                    change_type=ChangeType.PURCHASE,
                    quantity_change=detail.quantity,
                    source_type="PurchaseDetail",
                    source_id=detail.id,
                    user_id=user_id,
                    notes=f"Purchase received: {purchase.supplier_reference or purchase.id}"
                )
        
        db.commit()
        db.refresh(purchase)
        
        return purchase
    
    def add_payment(
        self,
        db: Session,
        purchase_id: str,
        payment_data: PaymentHistoryCreate,
        user_id: str
    ) -> PaymentHistory:
        """Add a payment to a purchase"""
        
        purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
        if not purchase:
            raise ValueError(f"Purchase {purchase_id} not found")
        
        # Create payment record
        payment = PaymentHistory(
            purchase_id=purchase_id,
            amount_paid=payment_data.amount_paid,
            payment_method=payment_data.payment_method,
            notes=payment_data.notes,
            created_by=user_id
        )
        
        db.add(payment)
        
        # Update payment status
        total_paid = sum(p.amount_paid for p in purchase.payments) + payment_data.amount_paid
        
        if total_paid >= purchase.total_price:
            purchase.payment_status = PaymentStatus.FULLY_PAID
        elif total_paid > 0:
            purchase.payment_status = PaymentStatus.PARTIALLY_PAID
        else:
            purchase.payment_status = PaymentStatus.UNPAID
        
        db.commit()
        db.refresh(payment)
        
        return payment
    
    def get_purchase(
        self,
        db: Session,
        purchase_id: str
    ) -> Optional[Purchase]:
        """Get a purchase by ID with all relationships"""
        return db.query(Purchase).options(
            joinedload(Purchase.supplier),
            joinedload(Purchase.details).joinedload(PurchaseDetail.product_variation).joinedload("product"),
            joinedload(Purchase.details).joinedload(PurchaseDetail.product_variation).joinedload("color"),
            joinedload(Purchase.payments),
            joinedload(Purchase.creator)
        ).filter(Purchase.id == purchase_id).first()
    
    def get_purchases(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        supplier_id: Optional[str] = None,
        status: Optional[PurchaseStatus] = None,
        payment_status: Optional[PaymentStatus] = None
    ) -> List[Purchase]:
        """Get purchases with optional filtering"""
        query = db.query(Purchase).options(
            joinedload(Purchase.supplier),
            joinedload(Purchase.creator)
        )
        
        if supplier_id:
            query = query.filter(Purchase.supplier_id == supplier_id)
        
        if status:
            query = query.filter(Purchase.status == status)
        
        if payment_status:
            query = query.filter(Purchase.payment_status == payment_status)
        
        return query.order_by(desc(Purchase.created_at)).offset(skip).limit(limit).all()
    
    def update_purchase(
        self,
        db: Session,
        purchase_id: str,
        update_data: PurchaseUpdate
    ) -> Purchase:
        """Update a purchase"""
        
        purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
        if not purchase:
            raise ValueError(f"Purchase {purchase_id} not found")
        
        update_dict = update_data.dict(exclude_unset=True)
        
        for field, value in update_dict.items():
            if value is not None:
                setattr(purchase, field, value)
        
        db.commit()
        db.refresh(purchase)
        
        return purchase
    
    def delete_purchase(
        self,
        db: Session,
        purchase_id: str
    ) -> bool:
        """Delete a purchase (only if status is DRAFT)"""
        
        purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
        if not purchase:
            return False
        
        if purchase.status != PurchaseStatus.DRAFT:
            raise ValueError("Can only delete draft purchases")
        
        db.delete(purchase)
        db.commit()
        
        return True


purchase_service = PurchaseService()
