from fastapi import APIRouter , Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..model.models import Response , Token
from ..model.user_model import User
from ..middleware.jwt import Login as Log
from datetime import datetime
from .utils import SetMetadataResponse
from ..model.models import MetadataResponse
from ..service.user_service import NewUserService

class NewPublicController():
    def __init__(self):
        self.__router:APIRouter = APIRouter(prefix="/api/v1/public", tags=["Public"])
        self.__res:Response = Response(metadata=MetadataResponse(messege="" , status=False , timeExecution=""))

    def GetRouter(self) -> APIRouter:
        @self.__router.post("/auth/login" , response_model=Token)
        def Login(credential_user: OAuth2PasswordRequestForm = Depends()):
            return Log(credential_user.username , credential_user.password)

        @self.__router.get("/auth/refresh")
        def Refresh():
            pass

        @self.__router.post("/user/register" , response_model=Response)
        def Register(user: User) -> Response:
            try:
                self.__res = NewUserService().UpsertAndHashPasword(False , user.dict(by_alias=True) , self.__res)
            except Exception as e:
                print(e)
                self.__res.metadata.messege = "Internal Server Error"
            finally:
                return SetMetadataResponse(datetime.now() , self.__res)
            
        @self.__router.post("/user/reset-pasword")
        def Reset_password():
            pass

        return self.__router