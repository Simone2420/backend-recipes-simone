# coding=utf-8
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

load_dotenv()

# URL de conexión, por defecto usando MySQL local
DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

# Pool recycle para prevenir cierres inesperados de MySQL
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
