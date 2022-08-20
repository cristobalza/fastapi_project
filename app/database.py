from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Specify Postgres Database location
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}'
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