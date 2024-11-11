from sqlalchemy import Integer, Column, Boolean, String
from database import base

class To_do(base):
    __tablename__ = 'to_do'
    id = Column(Integer, primary_key=True, index=True)
    Task = Column(String(50), unique=True)
    Status = Column(Boolean)
