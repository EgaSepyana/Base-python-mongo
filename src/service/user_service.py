from ..utils.database.pyMongo.mopy import MongoConnection
from ..model.user_model import User
from passlib.context import CryptContext
from ..model.models import Response , RequestPaginateion

class NewUserService:
    def __init__(self):
        self.__passwordContext:CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.__collname = "user"
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
            res.metadata.messege , res.data = self.__dbUtil.UpdateData({"_id" : param["_id"]}, param)
        else :
            res.metadata.messege , res.data = self.__dbUtil.InsertData(param)
        return res
    

    def hashPasword(self, password:str):
        return self.__passwordContext.hash(password)

    def verifyPassword(self,plain_password, hashed_password):
        return self.__passwordContext.verify(plain_password , hashed_password)
        
    def UpsertAndHashPasword(self, isUpdate:bool , param:dict , res:Response) -> Response:
        if not isUpdate:
            err , count = self.__dbUtil.CountDocument(
                {"username" : param["username"],
                "email": param["email"],
                }
                )
            if err != "":
                res.metadata.messege = err
            
            if count > 0:
                res.metadata.messege = "Username Or Email Already Exist"

            param["password"] = self.hashPasword(param["password"])
            

            res.metadata.messege , res.data = self.__dbUtil.InsertData(param)
        else :
            res.metadata.messege , res.data = self.__dbUtil.UpdateData({"_id" : param["_id"]} , param)

        return res