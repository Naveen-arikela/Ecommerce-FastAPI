from pydantic import BaseModel
from typing import Optional

class UserCreation(BaseModel):
    username: str
    email: str
    password: str

#Here we are not displaying password
class UserCreatedResponseModel(BaseModel):
    username: str
    email: str
    class Config:
        orm_mode = True
class DeleteUser(BaseModel):
    user_id: int
class TokenData(BaseModel):
    user_id: Optional[str] = None

class ProductsResponseModel(BaseModel):
    id: int
    product_name: str
    price: int
    user_id: int
    class Config:
        orm_mode = True

class Product(BaseModel):
    product_name: str
    price: int
    user_id: int