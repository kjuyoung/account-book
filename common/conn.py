from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Config DB connection
DB_CONN_URL = '{}://{}:{}@{}:{}/{}'.format(
    os.getenv("DB_TYPE"),
    os.getenv("DB_USER"),
    os.getenv("DB_PWD"),
    os.getenv("DB_HOST"),
    os.getenv("DB_PORT"),
    os.getenv("DB_NAME")
)

engine = create_engine(DB_CONN_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()