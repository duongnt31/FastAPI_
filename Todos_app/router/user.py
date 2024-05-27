from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter
from database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from model import Todos, Users
from passlib.context import CryptContext
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)

# explain: create a function that returns a database connection
def get_db():
    db = sessionLocal()
    try:
        yield db # explain: yield the db (yield is a keyword that is used to return a value, differrent from return, yield is used to return a generator)
    finally:
        db.close() # explain: close the db (close is a method that is used to close the connection to the database)\

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get('/todos', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password): # -> explain: verify the password 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error on password change")
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put("/phone_number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit() 
    
    
