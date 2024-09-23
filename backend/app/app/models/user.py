# # from .user_type import UserType

from db.db import Base, engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable = False, index = True)
    username = Column(String(35), unique=True, nullable=False) # Doubt: What about index?
    email = Column(String(35), unique=True)
    mobile_number = Column(String(12), unique=True)
    created_datetime = Column(DateTime, default=datetime.utcnow())
    hashed_password = Column(String(70), nullable=False)
    status_code = Column(Integer, default = 0)
    account_type = Column(String(15), default="Public")  # PUBLIC, FRIENDS
    otp_key = Column(String(60))

    profile = relationship("Profile", back_populates="user", uselist=False)
    post = relationship("Post", back_populates="user")
    post_like = relationship("PostLike", back_populates="user")
    comment = relationship("Comment", back_populates="user")
    otp_log = relationship("OtpLog", back_populates="user")
    sent_chat = relationship('Chat', foreign_keys='Chat.sender_id', back_populates='sender')
    received_chat = relationship('Chat', foreign_keys='Chat.receiver_id', back_populates='receiver')

