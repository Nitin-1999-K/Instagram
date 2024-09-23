from models import PostLike
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def getLike(db, post_id, user_id):
    return db.query(PostLike).filter(PostLike.post_id == post_id, PostLike.user_id == user_id).first()
    

def likePost(db: Session, post_id: int, user_id: int):
    try:
        like = PostLike(post_id = post_id, user_id = user_id)
        db.add(like)
        db.commit()
    except IntegrityError:
        pass


def getLikeById(db: Session, like_id: int):
    return db.query(PostLike).filter(PostLike.id == like_id).first()


def unlikePost(db: Session, post_like: PostLike):
    db.delete(post_like)
    db.commit()


def readLikesByPostId(db: Session, post_id):
    likes = db.query(PostLike).filter(PostLike.post_id == post_id).all()
    return likes


def readLikesByUserId(db: Session, user_id):
    likes = db.query(PostLike).filter(PostLike.user_id == user_id).all()
    return likes

