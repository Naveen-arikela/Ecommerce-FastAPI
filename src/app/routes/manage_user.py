from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..models import models
from ..schemas import schemas
from .login import get_current_user
from ..db.mysqldb import get_db
from ..constants import PWD_CONTEXT
from ..utils.common import wrap_response

router = APIRouter(
    tags=["Create User"]
)

# @router.post('/create-user', response_model=schemas.UserCreatedResponseModel)
@router.post('/create-user')
def create_user(request: schemas.UserCreationSchema, db: Session=Depends(get_db), user_auth: schemas.UserCreationSchema=Depends(get_current_user)):
    try:
        hashed_password = PWD_CONTEXT.hash(request.password)
        new_user = models.User(username=request.username, email=request.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return wrap_response(code=status.HTTP_201_CREATED, msg="Successfully created user")
    except Exception as e:
        return wrap_response(code=status.HTTP_400_BAD_REQUEST, msg=f"Exception: {e}")

#id as a query string parameter
@router.delete('/delete-user')
def delete_user(id, db: Session=Depends(get_db), user_auth: schemas.UserCreatedResponseModel=Depends(get_current_user)):
    try:
        user_info = db.query(models.User).filter(models.User.id == id)
        if not user_info.first():
            return wrap_response(code=status.HTTP_204_NO_CONTENT, msg="User not found")

        user_info.delete(synchronize_session=False)
        db.commit()
        return wrap_response(code=status.HTTP_200_OK, msg="Successfully deleted user")
    except Exception as e:
        return wrap_response(code=status.HTTP_400_BAD_REQUEST, msg=f"Exception: {e}")
    
    