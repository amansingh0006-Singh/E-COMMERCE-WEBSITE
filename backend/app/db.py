from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./ecom.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ✅ YAHI FUNCTION MISSING THA
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


























# cd backend/app
# uvicorn main:app --reload
# yhe run kare na kaam aata h ??