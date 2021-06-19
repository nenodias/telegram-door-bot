from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
 
 
Base = declarative_base()
 
 
class UserApartment(Base):
    __tablename__ = 'user_apartments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_name = Column(String)
    apartment = Column(Integer)