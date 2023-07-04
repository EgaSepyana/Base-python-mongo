from pydantic import BaseModel
from .models import MetadataWithId

class Role(MetadataWithId):
    name:str = ""
    description:str = ""
    privileges: dict | None = None