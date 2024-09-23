# # from .user_type import UserType

from db.db import Base, engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class Profile(Base):
    
    id = Column(Integer, primary_key=True)
    about = Column(String(100), nullable=True)
    profile_pic_directory = Column(String(150))
    profile_pic_datetime = Column(DateTime)
    location = Column(String(35))
    user_id = Column(Integer, ForeignKey("user.id"))
    status_code = Column(Integer, default = 1)
    
    user = relationship("User", back_populates="profile")
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
