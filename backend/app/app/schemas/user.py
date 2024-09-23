from pydantic import BaseModel
from fastapi import Body


class UserUpdate(BaseModel): 
    username: str | None = None
    email: str | None = None
    mobile_number: str | None = None
    name: str | None = None
    password: str | None = None
    account_type: str | None = None
    

class UserResetPassword(BaseModel):
    username: str | None = None
    email: str | None = None
    mobile_number: str | None = None

    @classmethod
    def init(cls, 
               username: str | None = Body(None),
               email: str | None = Body(None), 
               mobile_number: str | None = Body(None)):
        
        return cls(username = username,
                   email=email, 
                   mobile_number=mobile_number)