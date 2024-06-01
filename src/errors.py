from fastapi.routing import HTTPException
from fastapi import status
class HttpError(HTTPException):
    def to_dict(self):
        return {self.status_code: {"description":self.detail}}
class Status404(HttpError):

    def __init__(self,detail=None):
        self.status_code=status.HTTP_404_NOT_FOUND
        self.detail=detail


collar_not_found=Status404(detail="Could not find collar with this mac")
print(collar_not_found.to_dict())