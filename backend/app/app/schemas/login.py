from pydantic import BaseModel
from fastapi import Form, Body


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    email: str | None = None
    mobile_number: str | None = None
    name: str
    password: str

    @classmethod
    def init(cls, 
               name: str = Form(),
               username: str = Form(), 
               password: str = Form(), 
               email: str | None = Form(None), 
               mobile_number: str | None = Form(None)):
        
        return cls(name=name,
                   username = username, 
                   password=password, 
                   email=email if email else None, 
                   mobile_number=mobile_number if mobile_number else None)


class UserResetPassword(BaseModel):
    username: str | None = None
    email: str | None = None
    mobile_number: str | None = None

    @classmethod
    def init(cls, 
               username: str | None = Form(None),
               email: str | None = Form(None), 
               mobile_number: str | None = Form(None)):
        
        return cls(username = username,
                   email=email, 
                   mobile_number=mobile_number)


# class OTP(BaseModel):
#     otp_value : str
#     created_at: datetime = datetime.utcnow()
    

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class SignUpResponse(TokenResponse):
    otp: int