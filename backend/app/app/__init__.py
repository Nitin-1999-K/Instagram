# from pydantic import BaseModel
# from datetime import datetime
# # from fastapi import Form, Body


# class UserBase(BaseModel):
#     username: str


# class UserCreate(UserBase):
#     email: str | None = None
#     mobile_number: str | None = None
#     name: str
#     password: str

#     @classmethod
#     def init(cls, 
#                name: str,
#                username: str, 
#                password: str = Form(), 
#                email: str | None = None, 
#                mobile_number: str | None = None):
        
#         return cls(name=name,
#                    username = username, 
#                    password=password, 
#                    email=email, 
#                    mobile_number=mobile_number)



# class UserInDB(UserBase):
#     id: int
#     email: str | None = None
#     mobile_number: str | None = None
#     name: str
#     hashed_password: str
#     date_created: datetime
    


# class UserLogin(UserBase):
#     username: str | None = None
#     email: str | None = None
#     mobile_number: str | None = None
#     password: str

#     @classmethod
#     def init(cls, 
#                username: str | None = None, 
#                password: str = Form(), 
#                email: str | None = None, 
#                mobile_number: str | None = None):
        
#         return cls(username = username, 
#                    password=password, 
#                    email=email, 
#                    mobile_number=mobile_number)


# class UserUpdate(BaseModel):
#     username: str | None = None
#     email: str | None = None
#     mobile_number: str | None = None
#     name: str | None = None
#     password: str | None = None

#     @classmethod
#     def init(cls, 
#                name: str | None = None ,
#                username: str | None = None, 
#                password: str | None = Form(None), 
#                email: str | None = None, 
#                mobile_number: str | None = None):
        
#         return cls(name=name,
#                    username = username, 
#                    password=password, 
#                    email=email, 
#                    mobile_number=mobile_number)
    

# class UserResetPassword(BaseModel):
#     username: str | None = None
#     email: str | None = None
#     mobile_number: str | None = None

#     @classmethod
#     def init(cls, 
#                username: str | None = None,
#                email: str | None = None, 
#                mobile_number: str | None = None):
        
#         return cls(username = username,
#                    email=email, 
#                    mobile_number=mobile_number)
    

# class PostCreate(BaseModel):
#     text: str | None = None

#     @classmethod
#     def init(cls, 
               
#                text: str | None = Form(None)):
        
#         return cls(
#                    text=text)


# class OTP(BaseModel):
#     otp_value : str
#     created_at: datetime = datetime.utcnow()
    

# class PostUpdate(BaseModel):
#     id: int
#     text: str | None = None
#     files_to_delete: list[int] | None = None

#     @classmethod
#     def init(cls, 
#             id: int,
#             files_to_delete: str,
#             text: str | None = Body(None)
#             ):
        
#         return cls(id = id,
#                    text=text,
#                    files_to_delete = [int(i) for i in files_to_delete.split(",")])
    

# class PostRead(BaseModel):
#     id: int
#     text: str | None = None
#     files_to_delete: list[int] | None = None

#     @classmethod
#     def init(cls, 
#             id: int,
#             files_to_delete: str,
#             text: str | None = Body(None)
#             ):
        
#         return cls(id = id,
#                    text=text,
#                    files_to_delete = [int(i) for i in files_to_delete.split(",")])
    
    
# class PostResponse(BaseModel):
#     id: int
#     text: str
#     user_id: int
#     user_name: str
#     created_datetime: int
#     images: list | None = None

