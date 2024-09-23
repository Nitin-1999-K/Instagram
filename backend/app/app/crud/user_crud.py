from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from models import User as UserModel, Profile as ProfileModel, Post as PostModel, Image as ImageModel, Comment as CommentModel, PostLike as LikeModel, Chat as ChatModel
from schemas import UserCreate, UserUpdate
from . import profile_crud
from sqlalchemy.exc import IntegrityError
from core import security



def getUser(db: Session,
             username: str | None = None, 
             email: str | None = None, 
             mobile_number: str | None = None):

    user = db.query(UserModel).filter(
        or_(and_(UserModel.username == username, UserModel.username != None),
            and_(UserModel.email == email, UserModel.email != None),
            and_(UserModel.mobile_number == mobile_number, UserModel.mobile_number != None)
            )).first()
    return user



def createUser(db: Session, user: UserCreate):
    hashed_password = security.hash_password(user.password)
    try:
        db_user = UserModel(**user.model_dump(exclude = ("password")), 
                            hashed_password = hashed_password, status_code = 0)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()


def updateUser(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user == None:
        return None
    try:
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        if user.password:
            db_user.hashed_password = security.hash_password(user.password)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        return None
    return db_user


def deleteUser(db: Session, user: UserModel):
    user.status_code = -1
    db.query(ProfileModel).filter(ProfileModel.user_id == user.id).update({"status_code": -1})
    db.query(PostModel).filter(PostModel.user_id == user.id).update({"status_code": -1})
    images = db.query(ImageModel).join(PostModel).filter(PostModel.user_id == user.id).all()
    for image in images:
        setattr(image, "status_code", -1)
    db.query(LikeModel).filter(LikeModel.user_id == user.id).delete()
    db.query(CommentModel).filter(CommentModel.user_id == user.id).update({"status_code": -1})
    db.query(ChatModel).filter(ChatModel.sender_id == user.id).update({"status_code": -1})
    db.commit()

    

