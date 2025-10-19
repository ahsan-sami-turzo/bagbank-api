from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from typing import List, Optional
from app.models.product import Product, ProductVariation, OwnershipStatus
from app.models.supplier import Supplier, SupplierType
from app.schemas.product import ProductCreate, ProductUpdate, ProductVariationCreate
from app.utils.slug import generate_slug, ensure_unique_slug
from app.utils.sku import generate_sku


class ProductService:
    def create(self, db: Session, obj_in: ProductCreate) -> Product:
        """Create a new product with variations"""
        # Generate slug
        slug = generate_slug(obj_in.name)
        existing_slugs = [item.slug for item in db.query(Product).all()]
        unique_slug = ensure_unique_slug(slug, existing_slugs)
        
        # Create product data
        product_data = obj_in.dict(exclude={'variations'})
        product_data['slug'] = unique_slug
        
        # Create product
        db_obj = Product(**product_data)
        db.add(db_obj)
        db.flush()  # Flush to get the ID
        
        # Create variations
        for variation_data in obj_in.variations:
            # Generate SKU
            sku = self._generate_sku_for_variation(
                db, db_obj, variation_data.color_id
            )
            
            variation_obj = ProductVariation(
                product_id=db_obj.id,
                color_id=variation_data.color_id,
                sku=sku,
                stock_quantity=variation_data.stock_quantity
            )
            db.add(variation_obj)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: int) -> Optional[Product]:
        """Get a product by ID with all relationships"""
        return db.query(Product).options(
            joinedload(Product.category),
            joinedload(Product.material),
            joinedload(Product.brand),
            joinedload(Product.style),
            joinedload(Product.country),
            joinedload(Product.supplier),
            joinedload(Product.variations).joinedload(ProductVariation.color)
        ).filter(Product.id == id).first()
    
    def get_by_slug(self, db: Session, slug: str) -> Optional[Product]:
        """Get a product by slug with all relationships"""
        return db.query(Product).options(
            joinedload(Product.category),
            joinedload(Product.material),
            joinedload(Product.brand),
            joinedload(Product.style),
            joinedload(Product.country),
            joinedload(Product.supplier),
            joinedload(Product.variations).joinedload(ProductVariation.color)
        ).filter(Product.slug == slug).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        category_id: Optional[int] = None,
        brand_id: Optional[int] = None,
        ownership_status: Optional[OwnershipStatus] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[Product]:
        """Get multiple products with optional filtering"""
        query = db.query(Product).options(
            joinedload(Product.category),
            joinedload(Product.brand),
            joinedload(Product.supplier)
        )
        
        if category_id is not None:
            query = query.filter(Product.category_id == category_id)
        
        if brand_id is not None:
            query = query.filter(Product.brand_id == brand_id)
        
        if ownership_status is not None:
            query = query.filter(Product.ownership_status == ownership_status)
        
        if is_active is not None:
            query = query.filter(Product.is_active == is_active)
        
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                    Product.keywords.ilike(f"%{search}%")
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    def update(self, db: Session, db_obj: Product, obj_in: ProductUpdate) -> Product:
        """Update a product"""
        update_data = obj_in.dict(exclude_unset=True, exclude={'variations'})
        
        # If name is being updated, regenerate slug
        if 'name' in update_data and update_data['name'] != db_obj.name:
            slug = generate_slug(update_data['name'])
            existing_slugs = [
                item.slug for item in db.query(Product)
                .filter(Product.id != db_obj.id)
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
    
    def delete(self, db: Session, id: int) -> Optional[Product]:
        """Delete a product (soft delete by setting is_active=False)"""
        db_obj = db.query(Product).filter(Product.id == id).first()
        if db_obj:
            db_obj.is_active = False
            # Also deactivate all variations
            for variation in db_obj.variations:
                variation.is_active = False
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj
    
    def hard_delete(self, db: Session, id: int) -> Optional[Product]:
        """Permanently delete a product and its variations"""
        db_obj = db.query(Product).filter(Product.id == id).first()
        if db_obj:
            # Delete variations first (cascade should handle this)
            db.query(ProductVariation).filter(
                ProductVariation.product_id == id
            ).delete()
            
            db.delete(db_obj)
            db.commit()
        return db_obj
    
    def _generate_sku_for_variation(
        self, 
        db: Session, 
        product: Product, 
        color_id: int
    ) -> str:
        """Generate SKU for a product variation"""
        # Get color name
        from app.models.product_attributes import ProductColor
        color = db.query(ProductColor).filter(ProductColor.id == color_id).first()
        color_name = color.name if color else "UNKNOWN"
        
        return generate_sku(
            product_name=product.name,
            color_name=color_name,
            brand_name=product.brand.name,
            category_name=product.category.name,
            product_id=product.id
        )
    
    def get_suppliers_by_ownership(
        self, 
        db: Session, 
        ownership_status: OwnershipStatus
    ) -> List:
        """Get suppliers based on product ownership status"""
        if ownership_status == OwnershipStatus.OWNED:
            # Owned products should use factory suppliers
            return db.query(Supplier).filter(
                and_(
                    Supplier.supplier_type == SupplierType.FACTORY,
                    Supplier.is_active == True
                )
            ).all()
        else:
            # Not owned products should use wholesaler suppliers
            return db.query(Supplier).filter(
                and_(
                    Supplier.supplier_type == SupplierType.WHOLESALER,
                    Supplier.is_active == True
                )
            ).all()


product_service = ProductService()
