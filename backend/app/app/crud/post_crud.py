from fastapi import UploadFile
from sqlalchemy import or_, func
from sqlalchemy.orm import Session
from schemas import PostUpdate, PostResponse
from models import User as UserModel, Post as PostModel, Image as ImageModel, PostLike as LikeModel, Comment as CommentModel
from fastapi import UploadFile
from crud import image_crud
import json


def createPost(
    db: Session, 
    user_id: int, 
    text: str | None = None, 
    files: list[UploadFile] | None = None
):
    db_post = PostModel(user_id = user_id, text = text)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    if files:
        image_crud.uploadImages(db, post_id = db_post.id, files = files)


def readPosts(
    db: Session,
    user_id: int
):
    posts = db.query(PostModel.id, PostModel.text, PostModel.created_datetime, PostModel.user_id, UserModel.name.label("user_name"),  
    func.group_concat('{"id": ', ImageModel.id, ', "image_dir": "', ImageModel.image_dir, '"}')\
    .label('images')).join(UserModel).outerjoin(ImageModel).filter(or_(UserModel.account_type == "Public", 
    UserModel.id == user_id), PostModel.status_code == 1, or_(ImageModel.status_code == 1, 
    ImageModel.status_code == None)).group_by(PostModel.id).all()
    
    if posts:
        return [PostResponse(id=post.id, text=post.text, created_datetime = post.created_datetime, 
        user_id= post.user_id, user_name = post.user_name, images=json.loads(f'[{post.images}]') if post.images else [])
        for post in posts]


def readMyPosts( # Get current active user
    db: Session,
    user_id: int | None = None
):
    posts = db.query(PostModel.id, PostModel.text, PostModel.created_datetime, PostModel.user_id, UserModel.name.label("user_name"),  
    func.group_concat('{"id": ', ImageModel.id, ', "image_dir": "', ImageModel.image_dir, '"}')\
    .label('images')).join(UserModel).outerjoin(ImageModel).filter(UserModel.id == user_id, 
    PostModel.status_code == 1, or_(ImageModel.status_code == 1, ImageModel.status_code == None))\
    .group_by(PostModel.id).all()
    
    if posts:
        return [PostResponse(id=post.id, text=post.text, created_datetime = post.created_datetime, 
        user_id= post.user_id, user_name = post.user_name, images=json.loads(f'[{post.images}]') if post.images else [])
        for post in posts]


def readPost(
    db: Session,
    post_id: int,
    user_id: int
):
    post = db.query(PostModel.id, PostModel.text, PostModel.created_datetime, PostModel.user_id, UserModel.name.label("user_name"),  
    func.group_concat('{"id": ', ImageModel.id, ', "image_dir": "', ImageModel.image_dir, '"}')\
    .label('images')).join(UserModel).outerjoin(ImageModel).filter(or_(UserModel.account_type == "Public", 
    UserModel.id == user_id), PostModel.status_code == 1, PostModel.id == post_id, 
    or_(ImageModel.status_code == 1, ImageModel.status_code == None)).group_by(PostModel.id).first()
    
    if post:
        return PostResponse(id=post.id, text=post.text, created_datetime = post.created_datetime, 
        user_id= post.user_id, user_name = post.user_name, images=json.loads(f'[{post.images}]') if post.images else [])


def readMyPost(
    db: Session,
    user_id: int,
    post_id: int,
):
    post = db.query(PostModel.id, PostModel.text, PostModel.created_datetime, PostModel.user_id, UserModel.name.label("user_name"),  
    func.group_concat('{"id": ', ImageModel.id, ', "image_dir": "', ImageModel.image_dir, '"}')\
    .label('images')).join(UserModel).outerjoin(ImageModel).filter(UserModel.id == user_id, 
    PostModel.status_code == 1, PostModel.id == post_id, or_(ImageModel.status_code == 1, ImageModel.status_code == None))\
    .group_by(PostModel.id).first()
    
    if post:
        return PostResponse(id=post.id, text=post.text, created_datetime = post.created_datetime, 
        user_id= post.user_id, user_name = post.user_name, images=json.loads(f'[{post.images}]') if post.images else []) 


def getPostById(
    db: Session, 
    post_id: int, 
    status_code: int | None = None
):
    if status_code == None:
        post = db.query(PostModel).filter(PostModel.id == post_id).first()
    else:
        post = db.query(PostModel).filter(PostModel.id == post_id, PostModel.status_code == status_code).first()
    return post


def updatePost(
    db: Session,
    post: PostUpdate,
    db_post: PostModel,
    files: list[UploadFile] | None = None
):
    db_post.text = post.text
    if post.files_to_delete:
        image_crud.deleteImages(db, post_id = post.id, image_ids = post.files_to_delete)
    if files:
        image_crud.uploadImages(db = db, files = files, post_id = post.id)
    db.commit()



def deletePost(db: Session, post: PostModel):
    post.status_code = -1
    db.query(ImageModel).filter(ImageModel.post_id == post.id).update({"status_code": -1})
    db.query(LikeModel).filter(LikeModel.post_id == post.id).delete()
    db.query(CommentModel).filter(CommentModel.post_id == post.id).update({"status_code": -1})
    db.commit()










