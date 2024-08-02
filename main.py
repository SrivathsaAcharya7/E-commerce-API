from fastapi import FastAPI
from tortoise import models
from tortoise.contrib.fastapi import register_tortoise
from models import *

app=FastAPI()



@app.get("/")
def index():
    return {"Message":"Hello"}

register_tortoise(
    app,
    db_url="mysql://root:root@localhost:3306/ecommerce",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)