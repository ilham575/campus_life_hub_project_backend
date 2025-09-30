import os
from sqlalchemy import create_engine, text  
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# โหลดค่าจาก .env
load_dotenv()

# SQLite URL
SQLITE_DATABASE_URL = "sqlite:///./test.db"

# PostgreSQL URL (อ่านจาก .env)
POSTGRESQL_DATABASE_URL = os.getenv("POSTGRESQL_DATABASE_URL")

# เลือก DATABASE_URL
DATABASE_URL = POSTGRESQL_DATABASE_URL  # หรือเปลี่ยนเป็น SQLITE_DATABASE_URL ถ้าต้องการ

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("✅ Connected to DB:", result.scalar())
except Exception as e:
    print("❌ Database connection failed:", e)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()