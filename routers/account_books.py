from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import pyshorteners as ps

from common.conn import engine, get_db
from account_book.database import accountbook_models
from account_book.database import crud
from account_book.domain import schemas
from users.database import user_models
from routers.users import get_current_user

router = APIRouter(
    prefix="/api/v1"
)

accountbook_models.Base.metadata.create_all(bind = engine)

# Create a account book
@router.post("/accountbooks", status_code=status.HTTP_201_CREATED)
def create_account_book(request:schemas.AccountBookCreate, 
                        db: Session = Depends(get_db),
                        current_user: user_models.User = Depends(get_current_user)):
    found_account_book = crud.get_account_book(db, request=request)
    
    if found_account_book:
        raise HTTPException(status_code=409, detail="Account book record already registered")
    
    crud.create_account_book(db=db, account_book=request, user=current_user)

# Read account books list
@router.get("/accountbooks", response_model=list[schemas.ResponseRecord])
async def get_account_books(db: Session = Depends(get_db), 
                            skip: int = 0, 
                            limit: int = 20, 
                            current_user: user_models.User = Depends(get_current_user)):
    found_account_books = crud.get_account_books(db=db, skip=skip, limit=limit)

    if len(found_account_books) == 0:
        raise HTTPException(status_code=404, detail="Account book records not found")
    
    return found_account_books

# Read the account book by id
@router.get("/accountbooks/{account_book_id}", response_model=schemas.ResponseRecord)
def get_account_book_by_id(account_book_id: int, 
                           db: Session = Depends(get_db),
                           current_user: user_models.User = Depends(get_current_user)):
    found_account_book_by_id = crud.get_account_book_by_id(db, account_book_id=account_book_id)

    if found_account_book_by_id is None:
        raise HTTPException(status_code=404, detail="Account book record not found")
    
    return found_account_book_by_id

# Update the account book
@router.patch("/accountbooks/{account_book_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_account_book(account_book_id:int, 
                        request: schemas.AccountBook, 
                        db: Session = Depends(get_db),
                        current_user: user_models.User = Depends(get_current_user)):
    found_account_book = crud.get_account_book_by_id(db, account_book_id=account_book_id)

    if found_account_book is None:
        raise HTTPException(status_code=400, detail="Cannot update Account book record")
    
    crud.update_account_book(db=db, account_book_id=account_book_id, request=request, user=current_user)

# Delete the account book
@router.delete("/accountbooks/{account_book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account_book(account_book_id: int, 
                        db: Session = Depends(get_db),
                        current_user: user_models.User = Depends(get_current_user)):
    found_account_book = crud.get_account_book_by_id(db, account_book_id=account_book_id)

    if found_account_book is None:
        raise HTTPException(status_code=400, detail="Cannot delete Account book record")
    
    crud.delete_account_book(db=db, account_book_id=account_book_id, user=current_user)

# Copy the account book
@router.get("/accountbooks/{account_book_id}/copy", response_model=schemas.ResponseRecord)
def copy_account_book(account_book_id: int, 
                           db: Session = Depends(get_db),
                           current_user: user_models.User = Depends(get_current_user)):
    found_account_book = crud.get_account_book_by_id(db, account_book_id=account_book_id)

    if found_account_book is None:
        raise HTTPException(status_code=404, detail="Account book record not found")
    
    return found_account_book

# Share the short URL for the account book with the original URL
@router.get("/accountbooks/{account_book_id}/shareurl", status_code=status.HTTP_200_OK)
def share_account_book(account_book_id: int, 
                           db: Session = Depends(get_db),
                           current_user: user_models.User = Depends(get_current_user)):
    found_account_book = crud.get_account_book_by_id(db, account_book_id=account_book_id)

    if found_account_book is None:
        raise HTTPException(status_code=404, detail="Account book record not found")
    
    original_url = "http://localhost:8080/api/v1/accountbooks/" + str(account_book_id)
    
    sh = ps.Shortener()
    short_url = sh.tinyurl.short(original_url)
    
    return {
        "shortUrl": short_url,
        "originalUrl": original_url
    }