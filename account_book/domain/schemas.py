from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator

from users.domain import schemas


class AccountBookBase(BaseModel):
    expenditure: str
    memo: Optional[str] = None


class AccountBookCreate(AccountBookBase):
    pass

    @validator('expenditure')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class AccountBook(AccountBookBase):
    pass
    
    class Config:
        orm_mode = True
        

class ResponseRecord(AccountBookBase):
    id: int
    expenditure: str
    memo: Optional[str] = None
    create_date: datetime
    user: schemas.User | None
    modify_date: datetime | None = None
    
    
    class Config:
        orm_mode = True