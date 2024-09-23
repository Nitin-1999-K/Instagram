from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from api.deps import get_db
from crud import login_crud, user_crud
from core import security
from api import deps
import utils
from fastapi.security import OAuth2PasswordRequestForm
from models import User as UserModel 
from schemas import UserCreate, UserResetPassword as UserRP, SignUpResponse

router = APIRouter()


@router.post("/token", description = "To log-in")
def createAccessToken(db: Session = Depends(deps.get_db), user: OAuth2PasswordRequestForm = Depends()):

    db_user = user_crud.getUser(db, user.username)

    if not db_user:
        raise HTTPException(status_code=404, detail = "User not found")
    
    if db_user.status_code == -1:
        raise HTTPException(status_code=404, detail = "User not found")
    
    if not security.authenticate(user.password, db_user.hashed_password):
        raise HTTPException(status_code= 401, detail = "Incorrect Password")
    
    token = security.create_access_token(db_user.id)
    return {"access_token": token,"token_type": "bearer"}


@router.post("/signup", description = "To sign-up for the first time")
async def createUser(db: Session = Depends(deps.get_db), user: UserCreate = Depends(UserCreate.init)) -> SignUpResponse:

    if not user.email and not user.mobile_number:
        raise HTTPException(status_code=400, detail = "Either email or mobile number is mandatory")
    
    db_user = user_crud.createUser(db, user)

    if not db_user:

        db_user = user_crud.getUser(db, user.username, user.email, user.mobile_number)

        if db_user:
            signup_credentials = {"Username": user.username, 
                                 "E-mail": user.email, 
                                 "Mobile Number": user.mobile_number}
            db_credentials = {"Username": db_user.username, 
                             "E-mail": db_user.email, 
                             "Mobile Number": db_user.mobile_number}
            
            for credential in db_credentials:
                if db_credentials[credential] == signup_credentials[credential]:
                    raise HTTPException(status_code = 409,
                                        detail = f"{credential}: {db_credentials[credential]} already exists")
    
    db_user = login_crud.updateSecretKey(db, db_user) # Generating salt key for two-step verification
    otp = login_crud.generateOtp(db = db, otp_key = db_user.otp_key, user_id = db_user.id, otp_type = "SignUp")

    token = security.create_access_token(db_user.id)
    return {"access_token": token, "token_type": "bearer", "otp": otp}


@router.post("/verify-otp", description = "To verify otp send via mail after sign-up")
def verifyOtp(otp: int, db: Session = Depends(deps.get_db), user: UserModel = Depends(deps.get_current_user)): 
    if not user:
        raise HTTPException(status_code=401, detail = "Unauthorized user")
    if user.status_code == 1:
        raise HTTPException(409, "User already active")
    if user.status_code == -1:
        raise HTTPException(404, "Account not found")
    if utils.verifySignUpOtp(user.otp_key, otp):
        user = login_crud.activateAccount(db, user)
        {"detail": "Account activated"}
    {"detail": "OTP not validated"}
    

@router.post("/resend-otp", description = "To resend the otp") # status will be in Pending
def resendOtp(db: Session = Depends(deps.get_db), user: UserModel = Depends(deps.get_current_user)) -> int:
    if not user:
        raise HTTPException(401, "Request needs user to be authorized")
    if user.status_code == 1:
        raise HTTPException(409, "User already active")
    if user.status_code == -1:
        raise HTTPException(404, "Account not found")
    otp = login_crud.generateOtp(db = db, otp_key = user.otp_key, user_id = user.id, otp_type = "SignUp")
    return otp
# The otp depends upon randomly generated salt key for two-step verification


@router.post("/forgot-password", description = "To receive the link to reset the password") # User needs to be active
def forgotPassword(db: Session = Depends(deps.get_db), user: UserRP = Depends(UserRP.init)):
    if not user.username and not user.email and not user.mobile_number:
        raise HTTPException(status_code=400, detail="Either username or email or mobile number is mandatory")
    db_user = user_crud.getUser(db, **user.model_dump())
    if not db_user:
        raise HTTPException(status_code=404, detail = "User not found")
    token = utils.passwordResetToken(db_user.id)
    return utils.fakeSendEmail(token, db_user.email, db_user.mobile_number)


@router.post("/reset-password", description = "The actual link to reset the password")
def resetPassword(token: str, db: Session = Depends(deps.get_db), password: str = Form()):
    user = login_crud.passwordResetUser(db, token)
    if not user:
        raise HTTPException(404, detail = "User not found")
    if user.status_code == -1:
        raise HTTPException(410, "Account deleted")
    login_crud.setNewPassword(db, user, password)
    if security.authenticate(password,user.hashed_password):
        return {"detail": "Password Reset Successful"}