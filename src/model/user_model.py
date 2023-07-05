from .models import MetadataWithId
from pydantic import EmailStr

class User(MetadataWithId):
    roleId:str = ""
    email:EmailStr
    password:str
    username:str
    about:str = ""
    avatar:str = ""
    delete_status:str = "active"