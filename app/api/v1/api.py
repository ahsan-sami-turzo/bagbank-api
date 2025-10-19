from fastapi import APIRouter
from app.api.v1.endpoints import auth, product_attributes, supplier, product

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(product_attributes.router, prefix="/attributes", tags=["product-attributes"])
api_router.include_router(supplier.router, prefix="/suppliers", tags=["suppliers"])
api_router.include_router(product.router, prefix="/products", tags=["products"])

