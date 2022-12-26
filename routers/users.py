from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

from common.conn import engine, get_db
from users.database.crud import pwd_context
from users.domain import schemas
from users.database import crud
from users.database import user_models

router = APIRouter(
    prefix="/api/v1"
)

load_dotenv(override=True)

user_models.Base.metadata.create_all(bind = engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# for check user authority by using jwt
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, 
                                          detail="Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        # check jwt
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        # return authorized user information
        user = crud.get_user(db, email=email)
        if user is None:
            raise credentials_exception
        return user

# Create user
@router.post("/users/create", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    found_user = crud.get_existing_user(db, user_create=request)

    if found_user:
        raise HTTPException(status_code=409, detail="User already registered")

    crud.create_user(db=db, user_create=request)

# login for access token
@router.post("/users/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # check user and password
    user = crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    # return access token to login user
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user.email
    }

# logout
@router.post("/users/logout", status_code=status.HTTP_200_OK)
def logout():
    return {
        "detail": "logout"
    }