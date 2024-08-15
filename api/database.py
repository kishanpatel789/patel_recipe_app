from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

from .config import config_data

url = f"sqlite:///{config_data['db_path']}"

engine = create_engine(url, echo=True) # remove echo=True in prod
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# dependency function to get session object
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
