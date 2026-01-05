from fastapi import FastAPI
from db import Base, engine          # NEW: yahan se Base, engine
import models                        # NEW: models import (Product register ho jayega)
from  routers.products import router as products_router
from routers.users import router as users_router
from routers.cart import router as cart_router
from routers.orders import router as orders_router
from routers.admin import router as admin_router 




app = FastAPI(title="Test Ecom API")

# NEW: yahan tables create kara do
Base.metadata.create_all(bind=engine)

# products routes add
app.include_router(users_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(admin_router) 

@app.get("/")
def read_root():
    return {"message": "Backend is running fine!"}
