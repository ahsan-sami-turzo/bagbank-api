from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc
from typing import List, Optional
from decimal import Decimal
from app.models.stock import StockLedger, InventoryCount, ChangeType
from app.models.product import ProductVariation
from app.schemas.stock import StockLedgerCreate, InventoryCountCreate
from app.utils.sku import generate_sku


class StockService:
    def create_stock_entry(
        self,
        db: Session,
        product_variation_id: str,
        change_type: ChangeType,
        quantity_change: int,
        source_type: Optional[str] = None,
        source_id: Optional[str] = None,
        user_id: str = "system",
        notes: Optional[str] = None
    ) -> StockLedger:
        """Create a stock ledger entry and update current stock"""
        
        # Get current stock
        variation = db.query(ProductVariation).filter(
            ProductVariation.id == product_variation_id
        ).first()
        
        if not variation:
            raise ValueError(f"Product variation {product_variation_id} not found")
        
        current_stock = variation.current_stock
        new_balance = current_stock + quantity_change
        
        # Create stock ledger entry
        ledger_entry = StockLedger(
            product_variation_id=product_variation_id,
            change_type=change_type,
            source_type=source_type,
            source_id=source_id,
            quantity_change=quantity_change,
            running_balance=new_balance,
            user_id=user_id,
            notes=notes
        )
        
        db.add(ledger_entry)
        
        # Update current stock
        variation.current_stock = new_balance
        db.add(variation)
        
        db.commit()
        db.refresh(ledger_entry)
        
        return ledger_entry
    
    def get_stock_ledger(
        self,
        db: Session,
        product_variation_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[StockLedger]:
        """Get stock ledger entries with optional filtering"""
        query = db.query(StockLedger).options(
            joinedload(StockLedger.product_variation).joinedload(ProductVariation.product),
            joinedload(StockLedger.product_variation).joinedload(ProductVariation.color),
            joinedload(StockLedger.user)
        )
        
        if product_variation_id:
            query = query.filter(StockLedger.product_variation_id == product_variation_id)
        
        return query.order_by(desc(StockLedger.timestamp)).offset(skip).limit(limit).all()
    
    def get_current_stock(self, db: Session, product_variation_id: str) -> Optional[int]:
        """Get current stock for a product variation"""
        variation = db.query(ProductVariation).filter(
            ProductVariation.id == product_variation_id
        ).first()
        
        return variation.current_stock if variation else None
    
    def get_stock_summary(
        self,
        db: Session,
        low_stock_threshold: int = 10,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """Get stock summary for all product variations"""
        variations = db.query(ProductVariation).options(
            joinedload(ProductVariation.product),
            joinedload(ProductVariation.color)
        ).filter(ProductVariation.is_active == True).offset(skip).limit(limit).all()
        
        summary = []
        for variation in variations:
            total_value = float(variation.current_stock * variation.selling_price)
            is_low_stock = variation.current_stock <= low_stock_threshold
            
            summary.append({
                "product_variation_id": variation.id,
                "product_name": variation.product.name,
                "color_name": variation.color.name,
                "sku": variation.sku,
                "current_stock": variation.current_stock,
                "selling_price": float(variation.selling_price),
                "purchase_price": float(variation.purchase_price) if variation.purchase_price else None,
                "total_value": total_value,
                "is_low_stock": is_low_stock
            })
        
        return summary
    
    def create_inventory_count(
        self,
        db: Session,
        product_variation_id: str,
        counted_quantity: int,
        operator_id: str,
        notes: Optional[str] = None
    ) -> InventoryCount:
        """Create an inventory count and generate adjustment if needed"""
        
        # Get current system stock
        variation = db.query(ProductVariation).filter(
            ProductVariation.id == product_variation_id
        ).first()
        
        if not variation:
            raise ValueError(f"Product variation {product_variation_id} not found")
        
        system_stock = variation.current_stock
        difference = counted_quantity - system_stock
        
        # Create inventory count record
        inventory_count = InventoryCount(
            product_variation_id=product_variation_id,
            counted_quantity=counted_quantity,
            system_stock=system_stock,
            difference=difference,
            operator_id=operator_id,
            notes=notes
        )
        
        db.add(inventory_count)
        
        # If there's a difference, create adjustment entry
        if difference != 0:
            adjustment_entry = self.create_stock_entry(
                db=db,
                product_variation_id=product_variation_id,
                change_type=ChangeType.INVENTORY_COUNT,
                quantity_change=difference,
                source_type="InventoryCount",
                source_id=inventory_count.id,
                user_id=operator_id,
                notes=f"Inventory count adjustment: {difference:+d}"
            )
            
            inventory_count.adjustment_entry_id = adjustment_entry.id
        
        db.commit()
        db.refresh(inventory_count)
        
        return inventory_count
    
    def get_inventory_counts(
        self,
        db: Session,
        product_variation_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[InventoryCount]:
        """Get inventory count records with optional filtering"""
        query = db.query(InventoryCount).options(
            joinedload(InventoryCount.product_variation).joinedload(ProductVariation.product),
            joinedload(InventoryCount.product_variation).joinedload(ProductVariation.color),
            joinedload(InventoryCount.operator)
        )
        
        if product_variation_id:
            query = query.filter(InventoryCount.product_variation_id == product_variation_id)
        
        return query.order_by(desc(InventoryCount.count_date)).offset(skip).limit(limit).all()
    
    def get_low_stock_items(
        self,
        db: Session,
        threshold: int = 10
    ) -> List[dict]:
        """Get items with stock below threshold"""
        variations = db.query(ProductVariation).options(
            joinedload(ProductVariation.product),
            joinedload(ProductVariation.color)
        ).filter(
            and_(
                ProductVariation.is_active == True,
                ProductVariation.current_stock <= threshold
            )
        ).all()
        
        low_stock_items = []
        for variation in variations:
            low_stock_items.append({
                "product_variation_id": variation.id,
                "product_name": variation.product.name,
                "color_name": variation.color.name,
                "sku": variation.sku,
                "current_stock": variation.current_stock,
                "threshold": threshold
            })
        
        return low_stock_items


stock_service = StockService()
