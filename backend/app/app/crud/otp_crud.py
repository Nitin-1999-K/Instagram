from sqlalchemy.orm import Session
from models import OtpLog

def createOtpLog(db: Session, user_id: int, otp_type: int):
    otp = OtpLog(user_id = user_id, otp_type = otp_type)
    db.add(otp)
    db.commit()