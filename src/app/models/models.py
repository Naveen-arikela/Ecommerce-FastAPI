from sqlalchemy import(
    Column,
    Integer,
    String
)
from sqlalchemy.orm import relationship
from ..db.mysqldb import Base

# #Create table with the models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
   