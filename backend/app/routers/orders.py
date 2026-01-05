from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import Cart, Order, Product

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/{user_id}")
def place_order(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

    if not cart_items:
        raise HTTPException(400, "Cart is empty")

    total = 0

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if product.in_stock < item.quantity:
            raise HTTPException(400, f"{product.name} out of stock")

        product.in_stock -= item.quantity

        if product.in_stock == 0:
            product.is_available = 0

        total += product.price * item.quantity

    order = Order(user_id=user_id, total_amount=total)
    db.add(order)

    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()

    return {"message": "Order placed successfully", "total": total}
















































# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from db import get_db
# from models import Cart, Order, OrderItem, Product

# router = APIRouter(prefix="/orders", tags=["Orders"])


# @router.post("/{user_id}")
# def place_order(user_id: int, db: Session = Depends(get_db)):

#     cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

#     if not cart_items:
#         raise HTTPException(status_code=400, detail="Cart is empty")

#     total = 0
#     order = Order(user_id=user_id, total_amount=0)
#     db.add(order)
#     db.commit()
#     db.refresh(order)

#     for item in cart_items:
#         product = db.query(Product).filter(Product.id == item.product_id).first()
#         total += product.price * item.quantity

#         order_item = OrderItem(
#             order_id=order.id,
#             product_id=product.id,
#             quantity=item.quantity,
#             price=product.price
#         )
#         db.add(order_item)

#     order.total_amount = total
#     db.query(Cart).filter(Cart.user_id == user_id).delete()   # cart clear
#     db.commit()

#     return {
#         "message": "Order placed successfully",
#         "order_id": order.id,
#         "total_amount": total
#     }
