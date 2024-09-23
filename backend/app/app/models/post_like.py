from db.db import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

    
class PostLike(Base):
    __tablename__ = 'post_like'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    created_datetime = Column(DateTime, default=datetime.utcnow())

    user = relationship("User", back_populates="post_like")
    post = relationship("Post", back_populates="post_like")
