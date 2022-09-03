from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

DB_USERNAME= settings.database_username
DB_PASSWORD= settings.database_password
DB_HOSTNAME= settings.database_hostname
DB_NAME= settings.database_name
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
        
################################
# Documentation:
# Database Connection running Raw SQL on Postgress
################################
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time 
# while True:
#     try:
#         conn = psycopg2.connect(host=DB_HOSTNAME, 
#                                 database=DB_NAME,
#                                 user=DB_USERNAME,
#                                 password=DB_PASSWORD,
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database was connected succesfully!")
#         break
#     except Exception as error:
#         print("Connecting to Database failed.")
#         print(f"Error : {error}")
#         time.sleep(3)
################################