from jose import JWTError , jwt
from datetime import datetime , timedelta
from fastapi import HTTPException , Depends , status
from ..service.user_service import NewUserService
from fastapi.security.oauth2 import OAuth2PasswordBearer
from passlib.context import CryptContext
from ..utils.database.pyMongo.mopy import MongoConnection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/public/auth/login')
dbConnection:MongoConnection = MongoConnection.NewMongoConnectionLocal("user")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    token = data.copy()
    token.update( {"exp" : datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)} )

    encode_jwt = jwt.encode(token, SECRET_KEY , algorithm=ALGORITHM)
    
    token.update({"exp" : datetime.utcnow() + timedelta(days=7)})

    refresh_token = jwt.encode(token , SECRET_KEY , algorithm=ALGORITHM)

    return encode_jwt , refresh_token

def verify_access_token(token:str , credential_exception):

        try:
            payload = jwt.decode(token, SECRET_KEY , algorithms=ALGORITHM)
            id = payload.get("user_id")

            if not id:
                raise credential_exception
        except JWTError:
            raise credential_exception
        return id

def get_current_user(tokens:str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})

    decode_token = verify_access_token(token=tokens, credential_exception=credential_exception)
    
    user = dbConnection.GetOneDocument({"_id" : decode_token})
    return user

def Login(username , password):
    _ , user = dbConnection.GetOneDocument({"username" : username})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_FORBIDDEN, detail="Invalid Credentials")
    if not NewUserService().verifyPassword(password , user["password"]):
        raise HTTPException(status_code=status.HTTP_401_FORBIDDEN , detail="Wrong password")
    token , refresh_token = create_access_token(data={"user_id" : str(user.get("_id"))})
    return {"access_token" : token , "refresh_token" : refresh_token , "token_type" : "bearer"}
    