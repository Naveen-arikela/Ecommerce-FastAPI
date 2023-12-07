
from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List

from ..models import models
from ..schemas import schemas
from .login import get_current_user
from ..db.mysqldb import get_db
from ..constants import PWD_CONTEXT
from ..utils.common import wrap_response

router = APIRouter(
    tags=["Products"]
)

#return all products which are ordered by a user
# @router.get('/products', response_model=List[schemas.ProductsResponseModel])
@router.get('/products')
def get_products(db: Session=Depends(get_db), user_auth: schemas.UserCreatedResponseModel=Depends(get_current_user)):
    try:
        products = db.query(models.Product).all()
        if not products:
            return wrap_response(code=status.HTTP_204_NO_CONTENT, msg="Products not found", data=[])
        return wrap_response(code=status.HTTP_200_OK, msg="Success", data=products)
    except Exception as e:
        return wrap_response(code=status.HTTP_400_BAD_REQUEST, msg=f"Exception: {e}", data=[])

#add product
@router.post('/product', status_code=status.HTTP_201_CREATED)
def add_product(request: schemas.Product, db: Session=Depends(get_db), user_auth: schemas.UserCreatedResponseModel=Depends(get_current_user)):
    try:
        new_product = models.Product(product_name=request.product_name, price=request.price, user_id=request.user_id)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return wrap_response(code=status.HTTP_201_CREATED, msg="Successfully added product")
    except Exception as e:
        return wrap_response(code=status.HTTP_400_BAD_REQUEST, msg=f"Exception: {e}")

@router.put('/product/{id}')
def update_product(id, request: schemas.Product, db: Session=Depends(get_db), user_auth: schemas.UserCreatedResponseModel=Depends(get_current_user)):
    try:
        product = db.query(models.Product).filter(models.Product.id == id)
        if not product.first():
            return wrap_response(code=status.HTTP_204_NO_CONTENT, msg="Product not found")
        product.update(request.dict())
        db.commit()
        return wrap_response(code=status.HTTP_200_OK, msg="Successfully updated product")
    except Exception as e:
        return wrap_response(code=status.HTTP_400_BAD_REQUEST, msg=f"Exception: {e}")

@router.delete('/product/{id}')
def delete_product(id, db: Session=Depends(get_db), user_auth: schemas.UserCreatedResponseModel=Depends(get_current_user)):
    try:
        product = db.query(models.Product).filter(models.Product.id == id)
        if not product.first():
            return wrap_response(code=status.HTTP_204_NO_CONTENT, msg="Product not found")
        product.delete(synchronize_session=False)
        db.commit()
        return wrap_response(code=status.HTTP_200_OK, msg="Successfully deleted product")
    except Exception as e:
        return wrap_response(code=status.HTTP_400_BAD_REQUEST, msg=f"Exception: {e}")

