from ..service.role_service import NewRoleService
from ..model.models import MetadataResponse
from fastapi import APIRouter
from ..model.models import Response , RequestPaginateion
from ..model.role_model import Role
from datetime import datetime
from .utils import SetMetadataResponse

class NewRoleController():
    def __init__(self):
        self.__router:APIRouter = APIRouter(prefix="/api/v1/role", tags=["Role"])
        self.__res:Response = Response(metadata=MetadataResponse(messege="" , status=False , timeExecution=""))
        self.__service:NewRoleService = NewRoleService()

    def GetRouter(self) -> APIRouter:
        @self.__router.post("/get-all" , response_model=Response)
        def Get_All(req:RequestPaginateion):
            try:
                self.__res = self.__service.GetAll(self.__res , req)
            except:
                self.__res.metadata.messege = "Internal Server Error"
            finally:
                return SetMetadataResponse(datetime.now() , self.__res)

        @self.__router.get("/get-one" , response_model=Response)
        def Get_One(id: str):
            try:
                self.__res = self.__service.GetOne("_id" , id , self.__res)
            except:
                self.__res.metadata.messege = "Internal Server Error"
            finally:
                return SetMetadataResponse(datetime.now() , self.__res)

        @self.__router.post("/add" , response_model=Response)
        def Add(param: Role) -> Response:
            try:
                self.__res = self.__service.Upsert(False , param.dict(by_alias=True) , self.__res)
            except:
                self.__res.metadata.messege = "Internal Server Error"
            finally:
                return SetMetadataResponse(datetime.now() , self.__res)
                
            
        @self.__router.put("/update" , response_model=Response)
        def Update(param: Role):
            try:
                self.__res = self.__service.Upsert(True , param.dict(by_alias=True) , self.__res)
            except:
                self.__res.metadata.messege = "Internal Server Error"
            finally:
                return SetMetadataResponse(datetime.now() , self.__res)

        @self.__router.delete("/delete", response_model=Response)
        def DeleteOne(id :str):
            try:
                self.__res = self.__service.DeleteOne("_id" , id , self.__res)
            except Exception as e :
                print(e)
                self.__res.metadata.messege = "Internal Server Error"
            finally:
                return SetMetadataResponse(datetime.now() , self.__res)


        return self.__router

