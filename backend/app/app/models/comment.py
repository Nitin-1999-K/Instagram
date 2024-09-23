from db.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Comment(Base):

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    post_id = Column(Integer, ForeignKey("post.id"))
    text = Column(String(100), nullable = False)
    status_code = Column(Integer, default = 1)

    user = relationship("User", back_populates="comment")
    post = relationship("Post", back_populates="comment")
