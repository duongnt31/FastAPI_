from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter
from database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from model import Todos
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

# explain: create a function that returns a database connection
def get_db():
    db = sessionLocal()
    try:
        yield db # explain: yield the db (yield is a keyword that is used to return a value, differrent from return, yield is used to return a generator)
    finally:
        db.close() # explain: close the db (close is a method that is used to close the connection to the database)
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    return db.query(Todos).all()

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is not None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    
    