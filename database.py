from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite URL
SQLITE_DATABASE_URL = "sqlite:///./test.db"

# PostgreSQL URL (replace with your credentials)
POSTGRESQL_DATABASE_URL = "postgresql://username:password@localhost/dbname"

# Choose the database URL (SQLite or PostgreSQL)
DATABASE_URL = SQLITE_DATABASE_URL  # Change to POSTGRESQL_DATABASE_URL for PostgreSQL

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()