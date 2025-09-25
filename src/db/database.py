from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import getenv

load_dotenv()

db_pass = getenv("DB_PASSWORD")

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{db_pass}@db.hywkfqrxeuthzeaoywgt.supabase.co:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()