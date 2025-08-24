import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Use your actual password "root"
#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5432/qrdb")

# add render database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pravat:YntPdcOJ3s4JBaKi75H16IUWrf1I9Pt8@dpg-d2fka2ggjchc73fp7adg-a/opc_data")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Scan(Base):
    __tablename__ = "scans_tabale_1"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    name = Column(String, index=True)
    serial_num = Column(Integer, unique=True, index=True)  # Unique serial number
    timestamp = Column(DateTime, default=datetime.utcnow)
    unique_code = Column(String, index=True)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_next_serial():
    session = SessionLocal()
    try:
        max_serial = session.query(func.max(Scan.serial_num)).scalar()
        if max_serial is None:
            max_serial = 0
        return max_serial + 1
    finally:
        session.close()


def save_number(phone_number: str, name: str,unique_code:str):
    session = SessionLocal()
    try:
        serial_num = get_next_serial()
        scan = Scan(phone_number=phone_number, name=name, serial_num=serial_num,unique_code=unique_code)
        session.add(scan)
        session.commit()
        return serial_num
    finally:
        session.close()
