from sqlalchemy.orm import Session
from models import User as UserModel
from core import security
from crud import otp_crud, profile_crud
import utils
from api import deps


def updateSecretKey(db, db_user):
    otp_key = utils.createSecretKey()
    db_user.otp_key = otp_key
    db.commit()
    db.refresh(db_user)
    return db_user


def passwordResetUser(db: Session, token: str):
    token = utils.base64ToStr(token)
    return deps.get_current_user(db, token)


def setNewPassword(db: Session, user: UserModel, password: str):
    user.hashed_password = security.hash_password(password)
    db.commit()
    db.refresh(user)
    
    
def activateAccount(db, user):
    user.status_code = 1
    profile_crud.createProfile(db = db, user_id = user.id)
    db.commit()


def generateOtp(db: Session, otp_key: str, user_id: int, otp_type: str):
    otp = utils.generateOtp(otp_key) 
    otp_crud.createOtpLog(db = db, user_id = user_id, otp_type = otp_type)
    return otp