from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import SessionLocal
from models import Product

router = APIRouter(prefix="/products", tags=["Products"])


# ---------------------- DB Dependency ----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------- Pydantic Schemas ----------------------
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    in_stock: int = 0
    image_url: str | None = None


class ProductOut(ProductCreate):
    id: int

    class Config:
        # pydantic v2 style
        from_attributes = True


# ---------------------- Routes ----------------------

# GET /products/  -> saare products
@router.get("/", response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


# POST /products/  -> naya product create
@router.post("/", response_model=ProductOut)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    product = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        in_stock=product_in.in_stock,
        image_url=product_in.image_url,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# NEW: GET /products/{product_id} -> ek single product
@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# NEW: PUT /products/{product_id} -> product update
# Note: yaha hum pura object update kar rahe hain
# (name, description, price, in_stock, image_url sab bhejna padega)
@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product_in: ProductCreate,
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # fields update karo
    product.name = product_in.name
    product.description = product_in.description
    product.price = product_in.price
    product.in_stock = product_in.in_stock
    product.image_url = product_in.image_url

    db.commit()
    db.refresh(product)
    return product


# NEW: DELETE /products/{product_id} -> product delete
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
