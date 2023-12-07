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

    class config:
        orm_mode = True

class DeleteUser(BaseModel):
    user_id: int

class TokenData(BaseModel):
    user_id: Optional[str] = None