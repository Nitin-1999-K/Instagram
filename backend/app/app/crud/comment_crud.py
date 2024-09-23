from sqlalchemy import or_
from sqlalchemy.orm import Session
from models import Comment as CommentModel, Post as PostModel
from sqlalchemy.exc import IntegrityError


def addComment(
    user_id: int,
    text: str,
    post_id: int,
    db: Session
):
    try:
        comment = CommentModel(user_id = user_id, text = text, post_id = post_id)
        db.add(comment)
        db.commit()
    except IntegrityError:
        db.rollback()
        pass


def getCommentsByPostId(
    db: Session,
    post_id: int
):
    comments = db.query(CommentModel).select_from(PostModel).outerjoin(CommentModel, CommentModel.post_id == PostModel.id)\
    .filter(PostModel.id == post_id, or_(CommentModel.status_code == 1, CommentModel.status_code == None)).all()
    return comments


def getCommentById(
    db: Session,
    comment_id: int, 
    status_code: str | None = None):
    if status_code == None:
        comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    else:
        comment = db.query(CommentModel).filter(CommentModel.id == comment_id, CommentModel.status_code == status_code).first()
    return comment


def updateComment(
    db: Session,
    comment: CommentModel,
    text: str
):
    comment.text = text
    db.commit()


def deleteComment(
    comment: CommentModel,
    db: Session,
):
   comment.status_code = -1
   db.commit()
  
