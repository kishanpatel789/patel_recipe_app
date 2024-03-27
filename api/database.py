from sqlalchemy import create_engine
from sqlalchemy.engine import URL 
from sqlalchemy.orm import sessionmaker

from fastapi import HTTPException

from .config import config_data


url = URL.create(
    drivername="postgresql",
    username=config_data["username"],
    password=config_data["password"],
    host=config_data["host"],
    database=config_data["database"],
    port=5432,
)

schema_map = {None: config_data["schema"]}

engine = create_engine(url, echo=True).execution_options(schema_translate_map=schema_map) # remove echo=True in prod
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# dependency function to get session object
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
