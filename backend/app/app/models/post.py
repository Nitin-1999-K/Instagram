from db.db import Base, engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Post(Base):
    
    id = Column(Integer, primary_key=True)
    text = Column(String(100))
    created_datetime = Column(DateTime, default=datetime.utcnow())
    status_code = Column(Integer, default = 1)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="post")
    image = relationship("Image", back_populates="post")
    post_like = relationship("PostLike", back_populates="post")
    comment = relationship("Comment", back_populates="post")

