from pydantic import BaseModel
from datetime import datetime
from fastapi import Path, Body
from .post import PostResponse


class ProfileResponse(BaseModel):
    id: int
    about: str  | None = None
    profile_pic_directory: str  | None = None
    profile_pic_datetime: datetime  | None = None
    location: str  | None = None
    user_id: int
    status_code: int
    account_type: str
    posts: list[PostResponse | None] = []


class ProfileRequest(BaseModel):
    profile_id: int
    about: str  | None = None
    profile_pic_directory: str  | None = None
    profile_pic_datetime: datetime  | None = None
    location: str  | None = None
    
    @classmethod
    def init(cls, 
            profile_id: int = Path(),
            about: str  | None = Body(None),
            profile_pic_directory: str  | None = Body(None),
            location: str  | None = Body(None)
            ):
        
        return cls(profile_id = profile_id,
                   about=about,
                   profile_pic_directory = profile_pic_directory,
                   location = location
                )