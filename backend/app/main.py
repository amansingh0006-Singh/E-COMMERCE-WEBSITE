from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine          # NEW: yahan se Base, engine
import models                        # NEW: models import (Product register ho jayega)
from  routers.products import router as products_router

from routers.products import router as products_router
from routers.users import router as users_router
from routers.cart import router as cart_router
from routers.orders import router as orders_router
from routers.admin import router as admin_router


from models import User
from db import SessionLocal
from passlib.context import CryptContext   

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
app = FastAPI()

@app.post("/login")
def login(data: dict):

    email = data.get("email")
    password = data.get("password")

    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {
            "message": "User Not Found ❌"
        }

    if not pwd_context.verify(password, user.password):
        return {
            "message": "Wrong Password ❌"
        }

    return {
        "message": "Login Successful 🔥"
    }


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend Running 🔥"}
app.include_router(products_router) 
# app.include_router(users_router)
# app.include_router(cart_router)
# app.include_router(orders_router)
# app.include_router(admin_router)







# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )

# @app.post("/login")
# def login(data: dict):

#     email = data.get("email")
#     password = data.get("password")

#     db = SessionLocal()

#     user = db.query(User).filter(User.email == email).first()

#     if not user:
#         return {
#             "message": "User Not Found ❌"
#         }

#     if not pwd_context.verify(password, user.password):
#         return {
#             "message": "Wrong Password ❌"
#         }

#     return {
#         "message": "Login Successful 🔥"
#     }

