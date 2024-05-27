from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from model import Users
from passlib.context import CryptContext
from typing import Annotated
from database import sessionLocal
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'c3d81a96d4de607dc191bf270b2c21b8e6fbf05df402bf0693d4f807e909dd79'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreatUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

# explain: create a function that returns a database connection
def get_db():
    db = sessionLocal()
    try:
        yield db # explain: yield the db (yield is a keyword that is used to return a value, differrent from return, yield is used to return a generator)
    finally:
        db.close() # explain: close the db (close is a method that is used to close the connection to the database)


db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user

def create_access_token(username:str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency ,create_user_request: CreatUserRequest):
    create_user_model = Users (
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role = create_user_request.role,
        is_active = True,
        phone_number = create_user_request.phone_number
    )
    
    db.add(create_user_model)
    db.commit()
    
# Authenticate
@router.post("/token", response_model=Token) # -> explain: response_model is used to define the response model of the endpoint
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=15))
    
    return {"access_token": token, "token_type": "bearer"} # -> explain: return the access token and the token type (bearer is a type of token that is used to authenticate the user)