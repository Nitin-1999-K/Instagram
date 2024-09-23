import base64
import pyotp
from core import security
from models import User as UserModel
import os


def strToBase64(input_string):
    input_bytes = input_string.encode('utf-8')
    base64_bytes = base64.b64encode(input_bytes)
    url_safe_base64 = base64_bytes.decode('utf-8').replace('+', '-').replace('/', '_')
    return url_safe_base64


def base64ToStr(url_safe_base64):
    standard_base64 = url_safe_base64.replace('-', '+').replace('_', '/')
    base64_bytes = standard_base64.encode('utf-8')
    input_bytes = base64.b64decode(base64_bytes)
    original_string = input_bytes.decode('utf-8')
    return original_string


def createSecretKey():
    return pyotp.random_base32()


def passwordResetToken(user_id: int, expire_minutes: int | None = None):
    token = security.create_access_token(user_id, expire_minutes)
    return strToBase64(token)


def fakeSendEmail(token: str, email: str | None = None, mobile_number: str | None = None):
    if email:
        return f"Token: {token} sent to e-mail"
    elif mobile_number:
        return f"Token: {token} sent to mobile number"


def generateOtp(otp_key, interval = 60, digits = 6):
    print(otp_key)
    otp = pyotp.TOTP(otp_key, interval=interval, digits=digits).now()
    return otp


def verifySignUpOtp(otp_key: str, otp: int):
    print(otp_key)
    totp = pyotp.TOTP(otp_key, interval = 60)
    return totp.verify(otp)


def writeFile(file, filename, dir):
    image_path = os.path.join(dir, f"{filename}.jpg")
            
    with open(image_path, "wb") as buffer:  
        buffer.write(file.file.read())
