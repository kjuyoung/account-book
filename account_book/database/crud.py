from datetime import datetime
from sqlalchemy.orm import Session

from account_book.database import accountbook_models
from common import conn
from account_book.domain import schemas
from users.database import user_models

# for @router.get("/accountbooks")
def get_account_books(db: Session, skip: int, limit: int):
    
    return db.query(accountbook_models.AccountBook).offset(skip).limit(limit).all()

# for @router.post("/accountbooks")
def get_account_book(db: Session, request: schemas.AccountBookCreate):
    
    return db.query(accountbook_models.AccountBook).filter(accountbook_models.AccountBook.expenditure == request.expenditure and accountbook_models.AccountBook.memo == request.memo).first()

# for @router.get("/accountbooks/{account_book_id}")
def get_account_book_by_id(db: Session, account_book_id: int):
    
    return db.query(accountbook_models.AccountBook).filter(accountbook_models.AccountBook.id == account_book_id).first()

def get_account_book_by_memo(db: Session, account_book_memo: str):
    
    return db.query(accountbook_models.AccountBook).filter(accountbook_models.AccountBook.memo == account_book_memo).first()

# for @router.post("/accountbooks")
def create_account_book(db: Session, account_book: schemas.AccountBookCreate, user: user_models.User):
    create = accountbook_models.AccountBook(expenditure=account_book.expenditure, memo=account_book.memo)
    
    create.user = user
    
    db.add(create)
    db.commit()
    db.refresh(create)

# for @router.patch("/accountbooks/{account_book_id}")
def update_account_book(db: Session, account_book_id: int, request: schemas.AccountBook, user: user_models.User):
    update = db.query(accountbook_models.AccountBook).filter(accountbook_models.AccountBook.id == account_book_id).first()
    
    update.expenditure = request.expenditure
    update.memo = request.memo
    update.modify_date = datetime.now()
    
    db.add(update)
    db.commit()

# for @router.delete("/accountbooks/{account_book_id}")
def delete_account_book(db: Session, account_book_id: int, user: user_models.User):
    delete = db.query(accountbook_models.AccountBook).filter(accountbook_models.AccountBook.id == account_book_id).first()
    
    db.delete(delete)
    db.commit()