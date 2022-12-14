from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# IF using Alembic or other data migration tool, may leav below line commented
# ELSE whenever we start the application, SQLAlchemy will do either one of the folowing:
# 1. If there is a table with the names in models.py, it will do nothing
# 2. Else it will go ahead  and create the tables in Postgres. Check PGAdmin 
models.Base.metadata.create_all(bind=engine)

app  = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # what domains can talk to
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root(): 
    return {'message': 'Hello Worldd'}
