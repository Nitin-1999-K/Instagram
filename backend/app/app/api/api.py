from fastapi import APIRouter

from .endpoints import login, user, post, like, comment, chat, profile

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, tags=["user"])
api_router.include_router(post.router, tags=["posts"])
api_router.include_router(like.router, tags=["likes"])
api_router.include_router(comment.router, tags=["comments"])
api_router.include_router(chat.router, tags=["chats"])
api_router.include_router(profile.router, tags=["profile"])