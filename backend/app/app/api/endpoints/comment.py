from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from api.deps import get_db
from crud import comment_crud, post_crud
from api import deps
from models import User as UserModel
from schemas import CommentResponse

router = APIRouter(prefix = "/comments")


@router.post("/", status_code=201, description = "To comment on a particular post")
async def addComment(
    post_id: int,
    text: str = Form(),
    user: UserModel = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    if not post_crud.getPostById(db = db, post_id = post_id, status_code = 1):
            raise HTTPException(404, "Post not found")
    comment_crud.addComment(post_id = post_id, text = text, user_id = user.id, db = db)
    return {"detail": "Comment added"}


@router.get("/", description = "To view all the comments under a particular post")
def getCommentsByPostId(
    post_id: int,
    db: Session = Depends(deps.get_db)
) -> list[CommentResponse]:
    post = post_crud.getPostById(db = db, post_id = post_id, status_code = 1)
    if not post:
        raise HTTPException(404, "Post not found")
    comments = comment_crud.getCommentsByPostId(db , post_id)
    if comments == [None]:
        raise HTTPException(404, "No comments for this post")
    return comments


@router.patch("/{comment_id}", status_code=204, description = "To update a particular comment")
def updateComment(
    comment_id: int,
    text: str,
    db: Session = Depends(deps.get_db),
    user: UserModel = Depends(deps.get_current_active_user)
):
    comment = comment_crud.getCommentById(db = db, comment_id = comment_id, status_code = 1)
    if not comment:
        raise HTTPException(404, "Comment not found")
    if comment.user_id != user.id:
        raise HTTPException(401, "Can't modify other's comment")

    comment_crud.updateComment(db, comment, text)
    return {"detail": "Comment added"}


@router.delete("/{comment_id}", description = "To delete a particular comment")
def deleteComment(
    comment_id: int,
    db: Session = Depends(deps.get_db),
    user: UserModel = Depends(deps.get_current_active_user)
):
    comment =  comment_crud.getCommentById(comment_id = comment_id, db = db, status_code = 1)
    if not comment:
        raise HTTPException(404, "Comment not found")
    if comment.user_id != user.id:
        raise HTTPException(401, "Cannot delete other's comments")
    comment = comment_crud.deleteComment(comment = comment, db = db)
    return {"detail": "Comment deleted"}



