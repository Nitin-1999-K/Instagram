from db.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Chat(Base):
    
    id = Column(Integer, primary_key = True)
    sender_id = Column(Integer, ForeignKey("user.id"))
    receiver_id = Column(Integer, ForeignKey("user.id"))
    message = Column(String(100))
    status_code = Column(Integer, default=1)
    created_datetime = Column(DateTime, default=datetime.utcnow())

    sender = relationship('User', foreign_keys=[sender_id], back_populates='sent_chat')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='received_chat') 