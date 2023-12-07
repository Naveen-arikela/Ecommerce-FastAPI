from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas
from .login import get_current_user
from ..db.mysqldb import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    tags=["Create User"]
)

# @router.post('/create-user', response_model=schemas.UserCreatedResponseModel)
@router.post('/create-user')
def createUser(request: schemas.UserCreation, db: Session=Depends(get_db), current_user: schemas.UserCreation=Depends(get_current_user)):
    hashed_password = pwd_context.hash(request.password)
    new_user = models.User(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return "Successfully created user"

#id as a query string parameter
@router.delete('/delete-user')
def deleteUser(id, db: Session=Depends(get_db), current_user: schemas.UserCreatedResponseModel=Depends(get_current_user)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return "Successfully deleted user"
    