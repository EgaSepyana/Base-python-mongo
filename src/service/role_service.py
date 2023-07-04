from ..utils.database.pyMongo.mopy import MongoConnection
from ..model.role_model import Role
from ..model.models import Response , RequestPaginateion

class NewRoleService:
    def __init__(self):
        self.__collname = "role"
        self.__dbUtil:MongoConnection = MongoConnection.NewMongoConnectionLocal(self.__collname)

    def GetAll(self, res:Response , req:RequestPaginateion):
         res.data , res.metadata.pagination , res.metadata.messege = self.__dbUtil.FindAll(req)
         print(res.data)
         return res

    def GetOne(self, key:str , value:str , res:Response) -> Response:
        res.metadata.messege , res.data = self.__dbUtil.GetOneDocument({key : value})
        if not res.data:
            res.metadata.messege = "Data Not Found"

        return res

    def DeleteOne(self, key:str , value:str , res:Response):
         res.metadata.messege , res.data  = self.__dbUtil.DeleteOne({key : value})

         err , count = self.__dbUtil.CountDocument({key : value})
         
         if err != "":
             res.metadata.messege = err
         
         if type(count) == int and count < 1:
             res.metadata.messege = "Data Not Found"
           
         return res

    def Upsert(self, isUpdate:bool , param:dict , res:Response) -> Response:
        if isUpdate:
            res.metadata.messege , res.data = self.__dbUtil.UpdateData(param)
            return res
        
        res.metadata.messege , res.data = self.__dbUtil.InsertData(param)
        return res
        