from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import deps
from crud import post_like_crud, post_crud
from api import deps
from models import User as UserModel
from schemas import LikeResponse


router = APIRouter(prefix = "/likes")


@router.post("/{post_id}", description = "To like a particular post")
def likePost(
    post_id: int,
    user: UserModel = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
    ):
    if not user:
        raise HTTPException(401, "Request needs user to be authenticated")
    post = post_crud.getPostById(db = db, post_id = post_id, status_code=1)
    if not post:
        raise HTTPException(404, "Post not found")
    if post_like_crud.getLike(db = db, post_id = post_id, user_id = user.id):
            raise HTTPException(409, "Already liked this post")
    post_like_crud.likePost(db, user_id = user.id, post_id = post_id)
    return {"detail": "Like added"}


@router.get("/user", description = "To view all the posts liked by the user")
def readLikesByUserID(
    user: UserModel = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
) -> list[LikeResponse]:
    if not user:
        raise HTTPException(401, "Request needs user to be authenticated")
    likes = post_like_crud.readLikesByUserId(db = db, user_id = user.id)
    return likes


@router.get("/", description = "To view all the users who liked a particular post")
def readLikesByPostID(
    post_id: int,
    db: Session = Depends(deps.get_db)
) -> list[LikeResponse]:
    likes = post_like_crud.readLikesByPostId(db = db, post_id = post_id)
    return likes


@router.delete("/{like_id}", description = "To unlike a particular post")
def unlikePost(
    like_id: int,
    user: UserModel = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    if not user:
        raise HTTPException(401, "Request needs user to be authenticated")
    post_like = post_like_crud.getLikeById(db = db, like_id = like_id)
    if not post_like:
        raise HTTPException(404, "Like not found")
    if post_like.user_id != user.id:
        raise HTTPException(401, "Cannot remove other's post like")
    post_like_crud.unlikePost(db = db, post_like = post_like)
    return {"detail": "Post unliked"}