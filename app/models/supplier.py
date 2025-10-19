from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class SupplierType(str, enum.Enum):
    WHOLESALER = "wholesaler"
    FACTORY = "factory"


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    supplier_type = Column(Enum(SupplierType), nullable=False)
    name = Column(String(200), nullable=False)
    address = Column(String(500), nullable=True)
    contact_person = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    whatsapp_number = Column(String(20), nullable=True)
    email_address = Column(String(100), nullable=True)
    facebook_profile_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier(id={self.id}, name='{self.name}', type='{self.supplier_type}')>"
