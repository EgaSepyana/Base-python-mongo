from pydantic import BaseModel , Field

class MetadataWithId(BaseModel):
    id: str = Field(..., alias='_id')
    createdAt:int = 0
    updatedAt:int = 0


class RequestPaginateion(BaseModel):
    orderBy:str = "createdAt"
    order:str = "ASC"
    page:int = 1
    size:int = 11

class PaginationResponse (BaseModel):
    size:int
    totalPages:int
    totalElements:int

class MetadataResponse(BaseModel):
    status:bool
    messege:str
    timeExecution:str

    pagination:PaginationResponse | None = None

    class Config:
        orm_mode = True

class Response(BaseModel):
    metadata: MetadataResponse | None = None
    data: dict | list | str | None = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str