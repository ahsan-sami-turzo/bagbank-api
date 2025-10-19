from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum
import uuid


class OwnershipStatus(str, enum.Enum):
    OWNED = "yes"
    NOT_OWNED = "no"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(250), unique=True, index=True, nullable=False)
    
    # Foreign keys to product attributes
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("product_materials.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("product_brands.id"), nullable=False)
    style_id = Column(Integer, ForeignKey("product_styles.id"), nullable=False)
    country_id = Column(Integer, ForeignKey("countries_of_origin.id"), nullable=False)
    
    # Ownership and supplier
    ownership_status = Column(Enum(OwnershipStatus), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    
    # Pricing
    purchase_price = Column(Numeric(10, 2), nullable=True)
    selling_price = Column(Numeric(10, 2), nullable=False)
    
    # Content
    description = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)  # Comma-separated tags
    
    # Social media links
    youtube_video_url = Column(String(500), nullable=True)
    facebook_post_url = Column(String(500), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    category = relationship("ProductCategory", back_populates="products")
    material = relationship("ProductMaterial", back_populates="products")
    brand = relationship("ProductBrand", back_populates="products")
    style = relationship("ProductStyle", back_populates="products")
    country = relationship("CountryOfOrigin", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    variations = relationship("ProductVariation", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', slug='{self.slug}')>"


class ProductVariation(Base):
    __tablename__ = "product_variations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    color_id = Column(Integer, ForeignKey("product_colors.id"), nullable=False)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    barcode = Column(String(50), nullable=True)  # EAN/UPC code
    selling_price = Column(Numeric(10, 2), nullable=False)
    purchase_price = Column(Numeric(10, 2), nullable=True)  # Default cost
    initial_stock = Column(Integer, default=0)
    current_stock = Column(Integer, default=0)  # Computed and cached
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="variations")
    color = relationship("ProductColor", back_populates="variations")
    purchase_details = relationship("PurchaseDetail", back_populates="product_variation")
    purchase_returns = relationship("PurchaseReturn", back_populates="product_variation")
    sales_details = relationship("SalesDetail", back_populates="product_variation")
    stock_ledger_entries = relationship("StockLedger", back_populates="product_variation")
    inventory_counts = relationship("InventoryCount", back_populates="product_variation")

    def __repr__(self):
        return f"<ProductVariation(id={self.id}, sku='{self.sku}', product_id={self.product_id})>"
