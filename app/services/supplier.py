from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from app.models.supplier import Supplier, SupplierType
from app.schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:
    def create(self, db: Session, obj_in: SupplierCreate) -> Supplier:
        """Create a new supplier"""
        db_obj = Supplier(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: int) -> Optional[Supplier]:
        """Get a supplier by ID"""
        return db.query(Supplier).filter(Supplier.id == id).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        supplier_type: Optional[SupplierType] = None,
        is_active: Optional[bool] = None
    ) -> List[Supplier]:
        """Get multiple suppliers with optional filtering"""
        query = db.query(Supplier)
        
        if supplier_type is not None:
            query = query.filter(Supplier.supplier_type == supplier_type)
        
        if is_active is not None:
            query = query.filter(Supplier.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_type(
        self, 
        db: Session, 
        supplier_type: SupplierType,
        is_active: bool = True
    ) -> List[Supplier]:
        """Get suppliers by type (for dropdowns)"""
        return db.query(Supplier).filter(
            and_(
                Supplier.supplier_type == supplier_type,
                Supplier.is_active == is_active
            )
        ).all()
    
    def update(self, db: Session, db_obj: Supplier, obj_in: SupplierUpdate) -> Supplier:
        """Update a supplier"""
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if value is not None:
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> Optional[Supplier]:
        """Delete a supplier (soft delete by setting is_active=False)"""
        db_obj = db.query(Supplier).filter(Supplier.id == id).first()
        if db_obj:
            db_obj.is_active = False
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj
    
    def hard_delete(self, db: Session, id: int) -> Optional[Supplier]:
        """Permanently delete a supplier"""
        db_obj = db.query(Supplier).filter(Supplier.id == id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj


supplier_service = SupplierService()
