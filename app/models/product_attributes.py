from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<ProductCategory(id={self.id}, name='{self.name}', slug='{self.slug}')>"


class ProductMaterial(Base):
    __tablename__ = "product_materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="material")

    def __repr__(self):
        return f"<ProductMaterial(id={self.id}, name='{self.name}', slug='{self.slug}')>"


class ProductStyle(Base):
    __tablename__ = "product_styles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="style")

    def __repr__(self):
        return f"<ProductStyle(id={self.id}, name='{self.name}', slug='{self.slug}')>"


class ProductBrand(Base):
    __tablename__ = "product_brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="brand")

    def __repr__(self):
        return f"<ProductBrand(id={self.id}, name='{self.name}', slug='{self.slug}')>"


class ProductColor(Base):
    __tablename__ = "product_colors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    hex_code = Column(String(7), nullable=True)  # For HEX color codes like #FF5733
    rgb_code = Column(String(20), nullable=True)  # For RGB codes like rgb(255,87,51)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    variations = relationship("ProductVariation", back_populates="color")

    def __repr__(self):
        return f"<ProductColor(id={self.id}, name='{self.name}', slug='{self.slug}', hex='{self.hex_code}')>"


class CountryOfOrigin(Base):
    __tablename__ = "countries_of_origin"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="country")

    def __repr__(self):
        return f"<CountryOfOrigin(id={self.id}, name='{self.name}', slug='{self.slug}')>"
