from pydantic import BaseSettings

class Setings(BaseSettings):
    MONGO_SRV:str
    MONGO_DB:str
    
    class Config:
        env_file = ".env"

setings = Setings()