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

    update_credentials = {"Username": user_update.username, 
                          "E-mail": user_update.email, 
                          "Mobile Number": user_update.mobile_number}

    db_users = user_crud.getUsers(db, user.username, user.email, user.mobile_number)
    if db_users:
        for db_user in db_users:
            if db_user != user:
                db_credentials = {"Username": db_user.username, 
                                "E-mail": db_user.email, 
                                "Mobile Number": db_user.mobile_number}
                
                for credential in update_credentials:
                    if db_credentials[credential] and db_credentials[credential] == update_credentials[credential]:
                        raise HTTPException(status_code = 409,
                                            detail = f"{credential}: {db_credentials[credential]} already exists")
    user_crud.updateUser(db = db, user = user, user_update = user_update)
    return {"detail": "User updated"}


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