from fastapi import FastAPI
from tortoise import models
from tortoise.contrib.fastapi import register_tortoise
from models import *
from authentication import *
from typing import List,Optional,Type
from tortoise.signals import post_save
from tortoise import BaseDBAsyncClient

app=FastAPI()

@app.get("/")
def index():
    return {"Message":"Hello"}

@app.post("/registration")
async def user_registration(user:user_pydanticIn):
    user_info=user.dict(exclude_unset=True)
    user_info["password"]=get_hashed_password(user_info["password"])
    user_obj= await User.create(**user_info)
    new_user= await user_pydantic.from_tortoise_orm(user_obj)
    return {
        "status":"Ok",
        "Data":f"Hello{new_user.username}, thanks for registering with us. Please check your email inbox for verification mail."
    }

@post_save(User)
async def create_business(
        sender:"Type[User]",
        instance:User,
        created:bool,
        using_db:"Optional[BaseDBAsyncClient]",
        update_fields:List[str]
)->None:


register_tortoise(
    app,
    db_url="mysql://root:root@localhost:3306/ecommerce",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)