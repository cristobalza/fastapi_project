from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

DB_USERNAME= settings.db_username
DB_PASSWORD= settings.db_password
DB_HOSTNAME= settings.db_hostname
DB_NAME= settings.db_name
# Specify Postgres Database location
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL=f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}'
# engine is the responsible to connect ORM to Postgress DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# in order to talk to Postgres, we need a SessionLocal
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False, 
                            bind=engine)
# Base is extended to DB models
Base =  declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()