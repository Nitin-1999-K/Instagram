from pydantic import BaseModel
from datetime import datetime
from fastapi import Body


class PostUpdate(BaseModel):
    id: int
    text: str | None = None
    files_to_delete: list[int] | None = None

    @classmethod
    def init(cls, 
            id: int,
            files_to_delete: str,
            text: str | None = Body(None)
            ):
        
        return cls(id = id,
                   text=text,
                   files_to_delete = [int(i) for i in files_to_delete.split(",")])
    

class PostRead(BaseModel):
    id: int
    text: str | None = None
    files_to_delete: list[int] | None = None

    @classmethod
    def init(cls, 
            id: int,
            files_to_delete: str,
            text: str | None = Body(None)
            ):
        
        return cls(id = id,
                   text=text,
                   files_to_delete = [int(i) for i in files_to_delete.split(",")])
    
    
class ImageResponse(BaseModel):
    id: int
    image_dir: str


class PostResponse(BaseModel):
    id: int
    text: str
    user_id: int
    user_name: str
    created_datetime: datetime
    images: list[ImageResponse]