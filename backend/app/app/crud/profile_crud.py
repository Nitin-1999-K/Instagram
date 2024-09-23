from sqlalchemy import or_
from sqlalchemy.orm import Session
from models import User as UserModel, Profile as ProfileModel
from schemas import ProfileRequest
from crud import post_crud
from fastapi import UploadFile
from core.config import settings
from datetime import datetime
import utils


def createProfile(db: Session, user_id: int):
    db_profile = ProfileModel(user_id = user_id)
    db.add(db_profile)
    db.commit()


def readProfile(db: Session, profile_id: int, user_id: int):
    profile = db.query(ProfileModel).filter(ProfileModel.id == profile_id, ProfileModel.status_code == 1).first()
    if not profile:
        return profile
    if profile.user.account_type == "Public" or profile.user.id == user_id:
        profile = profile.as_dict() | {"account_type": profile.user.account_type}
        posts = post_crud.readMyPosts(db = db, user_id=profile["user_id"])
        if posts:
            profile["posts"] = posts
        return profile
    profile = profile.as_dict() | {"account_type": profile.user.account_type}
    return profile
  

def getProfileById(db: Session, profile_id: int):
    return db.query(ProfileModel).filter(ProfileModel.id == profile_id, ProfileModel.status_code == 1).first()


def updateProfile(db: Session, db_profile: ProfileModel, profile: ProfileRequest, profile_picture: UploadFile | None = None):
    for key, value in profile.model_dump(exclude_unset = True, exclude = {"profile_id"}).items():
        setattr(db_profile, key, value)
    
    if profile_picture:
        utils.writeFile(file = profile_picture, filename = db_profile.id, dir = settings.profile_pic_dir)
    
    db_profile.profile_pic_directory = settings.profile_pic_dir.replace("\\", "/") + f"/{str(db_profile.id)}"
    db_profile.profile_pic_datetime = datetime.utcnow()
    db.commit()