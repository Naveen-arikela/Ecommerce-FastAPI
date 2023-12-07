from sqlalchemy import(
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship
from ..db.mysqldb import Base

# #Create table with the models
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    price = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_relation = relationship("User", back_populates="products_relation")
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    products_relation = relationship("Product", back_populates="user_relation")

   