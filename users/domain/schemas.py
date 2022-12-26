from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password1: str
    password2: str

    @validator('email', 'password1', 'password2')
    def not_empty(cls, value):
        if (not value) or (not value.strip()):
            raise ValueError('빈 값은 허용되지 않습니다.')
        return value

    @validator('password2')
    def passwords_match(cls, v, values):
        if ('password1' in values) and (v != values['password1']):
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v


class User(UserBase):
    pass


    class Config:
        orm_mode = True
        

class ResponseUser(UserBase):
    id : int
    email: str
    create_date: datetime
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    email: str