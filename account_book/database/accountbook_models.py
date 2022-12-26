from datetime import datetime
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import sys

sys.path = ['', '..'] + sys.path[1:]

from common.conn import Base


class AccountBook(Base):
   __tablename__ = "accountbook_table"

   # Column id, expenditure, memo, create_date, user_id, modify_date
   id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
   expenditure = Column(String(255), nullable=False)
   memo = Column(Text, nullable=False)
   create_date = Column(DateTime, nullable=False, default=datetime.now())
   user_id = Column(BigInteger, ForeignKey("user.id"), nullable=True)
   user = relationship("User", backref="accountbooks")
   modify_date = Column(DateTime, nullable=True)

   def __init__(self, expenditure, memo):
      self.expenditure = expenditure
      self.memo = memo

   def __repr__(self):
      return "<Test('%d', '%s', '%s', '%s')>" % (self.id, self.expenditure, self.memo, self.create_date)