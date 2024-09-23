from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.deps import get_db
from schemas import UserUpdate
from crud import user_crud
from api import deps
from fastapi.security import OAuth2PasswordRequestForm
from models import User as UserModel

router = APIRouter(prefix = "/users")


@router.patch("/", description = "To update the credentials of the current user")
async def updateUser(
    user_update: UserUpdate,
    db: Session = Depends(deps.get_db),
    user: UserModel = Depends(deps.get_current_active_user)
):
    if not user:
        raise HTTPException(status_code=401, detail="Request needs user to be authorized")
    
    updated_user = user_crud.updateUser(db, user.id, user_update)
    if not updated_user:
        raise HTTPException(409, "Credentials already exist")
    return {"detail": "user updated"}


@router.delete("/", description = "To delete the user account")
async def deleteUser(
    db: Session = Depends(deps.get_db),
    user: UserModel = Depends(deps.get_current_user)
):
    if not user:
        raise HTTPException(status_code=401, detail="Not logged in")
    if user.status_code == -1:
        raise HTTPException(status_code=410, detail="Account already deleted")
    user_crud.deleteUser(db, user)
    return {"detail": "User deleted"}