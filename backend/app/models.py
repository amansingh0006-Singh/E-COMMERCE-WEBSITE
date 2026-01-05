from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
# ---------- USER TABLE ----------
class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Integer, default=0) 

# ---------- PRODUCT TABLE ----------
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    in_stock = Column(Integer, default=0)
    image_url = Column(String) 
    is_available =Column(Integer, default=1)


# -------- CART TABLE --------
class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)

# ---------- ORDER TABLE ----------
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    total_amount = Column(Integer)
    status = Column(String, default="PLACED")


# ---------- ORDER ITEMS ----------
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Integer)















# from sqlalchemy import Column, Integer, String, Text, Float
# from db import Base   # <- yaha change

# class Product(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(200), nullable=False)
#     description = Column(Text, nullable=True)
#     price = Column(Float, nullable=False)
#     in_stock = Column(Integer, default=0)
#     image_url = Column(String(500), nullable=True)
