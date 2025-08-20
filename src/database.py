import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Use your actual password "root"
#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5432/qrdb")

# add render database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pravat:YntPdcOJ3s4JBaKi75H16IUWrf1I9Pt8@dpg-d2fka2ggjchc73fp7adg-a/opc_data/")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_number(phone_number: str):
    session = SessionLocal()
    try:
        scan = Scan(phone_number=phone_number)
        session.add(scan)
        session.commit()
    finally:
        session.close()
