from fastapi import APIRouter, Depends, HTTPException, UploadFile
from api.deps import get_db
from sqlalchemy.orm import Session
from crud import profile_crud
from schemas import ProfileRequest
from models import User as UserModel
from api import deps
from schemas import ProfileResponse


router = APIRouter(prefix = "/profile")


@router.get("/", description = "To view a profile")
def readProfile(profile_id: int, db: Session = Depends(get_db), user: UserModel = Depends(deps.get_current_active_user)) -> ProfileResponse:
    profile = profile_crud.readProfile(db = db, profile_id = profile_id, user_id = user.id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    return profile


@router.patch("/{profile_id}", description = "To update the profile of the current user")
def updateProfile(profile_picture: UploadFile, 
                  profile: ProfileRequest = Depends(ProfileRequest.init),
                  db: Session = Depends(get_db),
                  user: UserModel = Depends(deps.get_current_active_user)):
    if not user:
        raise HTTPException(401, "Not Authenticated")
    db_profile = profile_crud.getProfileById(db = db, profile_id = profile.profile_id)
    if not db_profile:
        raise HTTPException(404, "Profile not found")
    if db_profile.user_id != user.id:
        raise HTTPException(401, "Can't alter other's profiles")
    profile_crud.updateProfile(db = db, db_profile = db_profile, profile = profile, profile_picture = profile_picture)
    return {"detail": "Profile updated"}

