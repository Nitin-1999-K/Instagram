from db.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class OtpLog(Base):

    __tablename__ = "otp_log"

    id = Column(Integer, primary_key=True)
    created_datetime = Column(DateTime, default=datetime.utcnow())
    otp_type = Column(String(15))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="otp_log")

