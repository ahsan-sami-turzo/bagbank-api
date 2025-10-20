from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, product_attributes, supplier, product,
    purchase, purchase_return_workflow, stock
)

api_router = APIRouter()

# Existing routes
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(product_attributes.router, prefix="/attributes", tags=["product-attributes"])
api_router.include_router(supplier.router, prefix="/suppliers", tags=["suppliers"])
api_router.include_router(product.router, prefix="/products", tags=["products"])
api_router.include_router(purchase.router, prefix="/purchases", tags=["purchases"])
api_router.include_router(
    purchase_return_workflow.router, 
    prefix="/purchase-returns", 
    tags=["purchase-returns"]
)
api_router.include_router(stock.router, prefix="/stock", tags=["stock"])

