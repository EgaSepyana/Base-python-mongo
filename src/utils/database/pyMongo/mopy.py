import pymongo
import uuid
from ....config.base import setings
import time
from pymongo.database import Database
from ....model.models import RequestPaginateion , PaginationResponse
from ..utils import GetSkipAndLimit , GetSortValue
import math

class MongoConnection:
    def __init__(self , srv:str , db_name:str , collection_name:str):
        self.__srv = srv
        self.__db_name = db_name
        self.__collection_name = collection_name

    @classmethod
    def NewMongoConnection(cls , srv:str , db_name:str , collection_name:str):
        return cls(srv , db_name , collection_name)
    
    @classmethod
    def NewMongoConnectionWithEnv(cls , collection_name):
        return cls(setings.MONGO_SRV , setings.MONGO_DB , collection_name)
    
    @classmethod
    def NewMongoConnectionLocal(cls , collection_name):
        return cls("mongodb://localhost:27017" , "tmp-data" , collection_name)

    def Conection(self) -> Database:
        client = pymongo.MongoClient(self.__srv)
        db = client[self.__db_name]
        return db

    def InsertData(self, data:dict , collactionName = ""):
        try :
            db = self.Conection()
            data["_id"] = uuid.uuid4().hex
            data["updatedAt"] = int(time.time() * 1000)
            data["createdAt"] = int(time.time() * 1000)
            data["delete_status"] = "active"
            res = db[collactionName if collactionName != "" else self.__collection_name].insert_one(data)
            return "" , res.inserted_id
        except Exception as i:
            print(i)
            return "Error Inserted Data" , ""
        
    def UpdateData(self ,querry:dict, data:dict):
        try:
            db = self.Conection()
            data["updatedAt"] = int(time.time() * 1000)
            res = db[self.__collection_name].update_one(querry , { "$set": data })
            return "" , data.get("_id")
        except Exception as i:
            print(i)
            return "Error Inserted Data" , ""
    
    def InsertDataByUsingId(self , data:dict , id:str):
        try :
            db = self.Conection()
            data["_id"] = id
            res = db[self.__collection_name].insert_one(data)
            return "" , res.inserted_id
        except Exception as i:
            print(i)
            return "Error Inserted Data" , ""
    def CountDocument(self , query:dict):
        try:
           db = self.Conection()
           res = db[self.__collection_name].count_documents(query)
           return "" , res 
        except Exception as i:
            print(i)
            return "Error Count Document" , ""
        
    def GetOneDocument(self , query:dict):
        try:
           db = self.Conection()
           res = db[self.__collection_name].find_one(query)
           return "" , res
        except Exception as i:
            print(i)
            return "Error Get Document" , ""
        
    def DeleteOne(self , query:dict):
        try:
           db = self.Conection()
           res = db[self.__collection_name].update_one(query , { "$set": {"delete_status" : "archive"} })
           return "" , res.upserted_id
        except Exception as i:
            print(i)
            return "Error Delete Document" , ""
        
    def FindAll(self, request:RequestPaginateion):
        try:
           query = {"delete_status" : {"$ne" : "archive"}}
           _ , totalElement = self.CountDocument(query=query)
           db = self.Conection()
           skip, limit = GetSkipAndLimit(request)
           res = db[self.__collection_name].find(query).skip(skip).limit(limit).sort(request.orderBy if request.orderBy != "" else "updatedAt", GetSortValue(request))
           return list(res) , PaginationResponse(size=limit , totalElements=totalElement , totalPages=math.ceil(totalElement / limit)) , ""
        except Exception as i:
            print(i)
            return None,None,"Error Find Document"