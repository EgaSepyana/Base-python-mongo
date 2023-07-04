from ...model.models import RequestPaginateion

def GetSkipAndLimit(request: RequestPaginateion):
    skip = request.page
    if skip > 0:
        skip -= 1
    
    skip *= request.size
    
    limit = request.size
    if limit == 0:
        limit = 10

    return skip , limit

def GetSortValue(request: RequestPaginateion):
    order = -1
    if request.order.lower() == "asc":
        order = 1
    
    return order