from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import Optional
# from typing import List

from routers import users, account_books

app = FastAPI(
    title="Account Book API",
    description="Account Book CRUD API project",
    version="0.0.1"
)
app.include_router(users.router)
app.include_router(account_books.router)