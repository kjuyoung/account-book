from datetime import datetime
from sqlalchemy import BigInteger, Column, String, DateTime, Text
from sqlalchemy import Column, String

from common.conn import Base


class User(Base):
    __tablename__ = "user"
    
    # Column id, email, password, create_date
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now())
    
    def __init__(self, email, password):
       self.email = email
       self.password = password

    def __repr__(self):
       return "<Test('%d', '%s', '%s')>" % (self.id, self.email, self.create_date)