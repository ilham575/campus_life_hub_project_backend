import os
from sqlalchemy import create_engine, text  
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# โหลดค่าจาก .env
load_dotenv()

# SQLite URL
SQLITE_DATABASE_URL = "sqlite:///:memory:"   # ใช้ in-memory DB เร็วและไม่ต้องสร้างไฟล์

# PostgreSQL URL (อ่านจาก .env)
POSTGRESQL_DATABASE_URL = os.getenv("POSTGRESQL_DATABASE_URL")

# เลือก DATABASE_URL ตามสภาพแวดล้อม
if os.getenv("RUN_TEST") == "1":
    DATABASE_URL = SQLITE_DATABASE_URL
else:
    DATABASE_URL = POSTGRESQL_DATABASE_URL

# Create the database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

try:
    with engine.connect() as conn:
        if "sqlite" in DATABASE_URL:
            result = conn.execute(text("SELECT sqlite_version();"))
        else:
            result = conn.execute(text("SELECT version();"))
        print("✅ Connected to DB:", result.scalar())
except Exception as e:
    print("❌ Database connection failed:", e)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
