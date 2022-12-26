from sqlalchemy.orm import Session
from passlib.context import CryptContext

from users.database import user_models
from users.domain import schemas
from common import conn

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# for @router.post("/users/login")
def get_user(db: Session, email: str):
    
    return db.query(user_models.User).filter(user_models.User.email == email).first()

# for @router.post("/users/create")
def get_existing_user(db: Session, user_create: schemas.UserCreate):
    
    return db.query(user_models.User).filter(user_models.User.email == user_create.email).first()

# for @router.post("/users/create")
def create_user(db: Session, user_create: schemas.UserCreate):
    db_user = user_models.User(email=user_create.email, password=pwd_context.hash(user_create.password1))
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)