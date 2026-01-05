from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import Product, Order

router = APIRouter(prefix="/admin", tags=["Admin"])


def admin_required(user_id: int, db: Session):
    from models import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.is_admin != 1:
        raise HTTPException(status_code=403, detail="Admin access only")


@router.get("/products/{user_id}")
def get_all_products(user_id: int, db: Session = Depends(get_db)):
    admin_required(user_id, db)
    return db.query(Product).all()


@router.get("/orders/{user_id}")
def get_all_orders(user_id: int, db: Session = Depends(get_db)):
    admin_required(user_id, db)
    return db.query(Order).all()
