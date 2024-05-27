import sys
sys.path.append('/home/duong/Documents/Training/Fastapi/Training/Todos_app')

from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from database import engine
from router import auth, todos, admin, user

app = FastAPI()

Base = declarative_base() # explain: create a Base class (a Base class is a class that is used to create a model class)

Base.metadata.create_all(bind=engine) # explain: create the database

app.include_router(auth.router) # explain: include the auth router
app.include_router(todos.router) # explain: include the todos router
app.include_router(admin.router) # explain: include the admin router
app.include_router(user.router) # explain: include the user router


