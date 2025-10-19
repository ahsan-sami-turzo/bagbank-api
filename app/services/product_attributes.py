from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional, Type, TypeVar
from app.models.product_attributes import (
    ProductCategory, ProductMaterial, ProductStyle, 
    ProductBrand, ProductColor, CountryOfOrigin
)
from app.schemas.product_attributes import (
    ProductCategoryCreate, ProductCategoryUpdate,
    ProductMaterialCreate, ProductMaterialUpdate,
    ProductStyleCreate, ProductStyleUpdate,
    ProductBrandCreate, ProductBrandUpdate,
    ProductColorCreate, ProductColorUpdate,
    CountryOfOriginCreate, CountryOfOriginUpdate
)
from app.utils.slug import generate_slug, ensure_unique_slug

ModelType = TypeVar('ModelType')


class ProductAttributeService:
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def create(self, db: Session, obj_in: dict) -> ModelType:
        """Create a new product attribute"""
        # Generate slug
        slug = generate_slug(obj_in['name'])
        
        # Ensure slug is unique
        existing_slugs = [item.slug for item in db.query(self.model).all()]
        unique_slug = ensure_unique_slug(slug, existing_slugs)
        
        # Create object
        obj_data = obj_in.copy()
        obj_data['slug'] = unique_slug
        
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a product attribute by ID"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_by_slug(self, db: Session, slug: str) -> Optional[ModelType]:
        """Get a product attribute by slug"""
        return db.query(self.model).filter(self.model.slug == slug).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[ModelType]:
        """Get multiple product attributes with optional filtering"""
        query = db.query(self.model)
        
        if is_active is not None:
            query = query.filter(self.model.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    def update(self, db: Session, db_obj: ModelType, obj_in: dict) -> ModelType:
        """Update a product attribute"""
        update_data = obj_in.copy()
        
        # If name is being updated, regenerate slug
        if 'name' in update_data and update_data['name'] != db_obj.name:
            slug = generate_slug(update_data['name'])
            existing_slugs = [
                item.slug for item in db.query(self.model)
                .filter(self.model.id != db_obj.id)
                .all()
            ]
            update_data['slug'] = ensure_unique_slug(slug, existing_slugs)
        
        for field, value in update_data.items():
            if value is not None:
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> Optional[ModelType]:
        """Delete a product attribute (soft delete by setting is_active=False)"""
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if db_obj:
            db_obj.is_active = False
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj
    
    def hard_delete(self, db: Session, id: int) -> Optional[ModelType]:
        """Permanently delete a product attribute"""
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj


# Service instances for each model
category_service = ProductAttributeService(ProductCategory)
material_service = ProductAttributeService(ProductMaterial)
style_service = ProductAttributeService(ProductStyle)
brand_service = ProductAttributeService(ProductBrand)
color_service = ProductAttributeService(ProductColor)
country_service = ProductAttributeService(CountryOfOrigin)
