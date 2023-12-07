from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..models import models
from ..schemas import schemas
from ..db.mysqldb import get_db
from ..constants import(
    SECRET_KEY,
    ALGORITHEM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    PWD_CONTEXT
)
from ..utils.common import wrap_response

from datetime import datetime, timedelta
from jose import jwt, JWTError

router = APIRouter(tags=["Login"])
oauth2_schme = OAuth2PasswordBearer(tokenUrl="login")

def generate_token(data: dict):
    to_encode = data.copy()
    token_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": token_expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHEM)
    return encoded_jwt

@router.post('/login')
def login(request: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    print(f"login:: user_id::{user.id}")

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not PWD_CONTEXT.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    access_token = generate_token(
        data={
            "sub": str(user.id)
        }
    )
    print(f"login:: access_token: {access_token}")
    response = {
        "access_token": access_token,
        "token_type": "bearer"
    }
    return response

def get_current_user(token: str=Depends(oauth2_schme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    print(f"get_current_user:: token: {token}")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHEM])
        print(f"get_current_user:: payload: {payload}")

        user_id: str = payload.get('sub')
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
        