from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Cart, Product

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/{user_id}")
def view_cart(user_id: int, db: Session = Depends(get_db)):
    cart_items = (
        db.query(Cart, Product)
        .join(Product, Cart.product_id == Product.id)
        .filter(Cart.user_id == user_id)
        .all()
    )

    response = []
    grand_total = 0

    for cart, product in cart_items:
        total_price = product.price * cart.quantity
        grand_total += total_price

        response.append({
            "cart_id": cart.id,
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": cart.quantity,
            "total_price": total_price,
            "image": product.image_url
        })

    return {
        "user_id": user_id,
        "items": response,
        "grand_total": grand_total
    }




































# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from db import get_db
# from models import Cart

# router = APIRouter(prefix="/cart",tags=["Cart"])

# @router.post("/add")
# def add_to_cart(
#     user_id: int,
#     product_id: int,
#     quantity: int = 1,
#     db: Session = Depends(get_db)
# ):
#     cart_item = Cart(
#         user_id=user_id,
#         product_id=product_id,
#         quantity=quantity
#     )

#     db.add(cart_item)
#     db.commit()
#     db.refresh(cart_item)

#     return {"message": "Product added to cart"}
