from datetime import datetime
from ..model.models import Response
from fastapi import status
from fastapi.responses import JSONResponse

def SetMetadataResponse(strtime:datetime , res:Response) -> Response:
    res.metadata.status = True

    if not res.data:
        res.data = None
        
    if res.metadata.messege == "":
        res.metadata.messege = "OK"
    else:
        res.metadata.status  = False
        res.metadata.timeExecution = f"{(datetime.now() - strtime).total_seconds() * 10**3}ms"
        if res.metadata.messege.lower() == "internal server error":
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , content=res.dict())
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST , content=res.dict())

    res.metadata.timeExecution = f"{(datetime.now() - strtime).total_seconds() * 10**3}ms"
    return res