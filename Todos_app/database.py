from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db' # explain: create a database file called todos.db

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123456@localhost/TodoApplicationDatabase' # explain: create a database called todosapp

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) # explain: create a database connection

engine = create_engine(SQLALCHEMY_DATABASE_URL) 

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # explain: create a sessionLocal (a sessionLocal is a class that is used to create a session object)

Base = declarative_base() # explain: create a Base class (a Base class is a class that is used to create a model class)

