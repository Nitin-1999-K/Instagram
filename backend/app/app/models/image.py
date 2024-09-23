from db.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.config import settings

class Image(Base):

    id = Column(Integer, primary_key=True)
    image_dir = Column(String(150))
    created_datetime = Column(DateTime, default=datetime.utcnow())
    status_code = Column(Integer, default = 1)

    post_id = Column(Integer, ForeignKey("post.id"))
    profile_id = Column(Integer, ForeignKey("profile.id"))
    
    post = relationship("Post", back_populates="image")
