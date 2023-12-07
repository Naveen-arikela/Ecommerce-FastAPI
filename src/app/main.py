from fastapi import FastAPI
from .routes import login, manage_user, products
from .models import models
from .db.mysqldb import engine

app = FastAPI(
    title="Ecommerce Fast API",
    # description="Add items in to the cart",
    contact={
        "Developer name": "Naveen Arikela",
        "email": "arikelanaveen11@gmail.com",
        "website": "http://makes.org.in"
    }
)

#Add external app routes here
app.include_router(login.router)
app.include_router(manage_user.router)
app.include_router(products.router)

#Create tables
models.Base.metadata.create_all(engine)
