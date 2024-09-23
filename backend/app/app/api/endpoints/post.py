from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from schemas import PostUpdate, PostResponse
from crud import post_crud
from api import deps
from models import User as UserModel 

router = APIRouter(prefix = "/posts")


@router.post("/create-post", status_code=201, description = "To make a post")
async def createPost(
    text: str | None = None,
    db: Session = Depends(deps.get_db),
    user: UserModel = Depends(deps.get_current_active_user),
    files: list[UploadFile] = File()
):
    if not user:
        raise HTTPException(status_code=401, detail="Request needs user to be authorized")
    if not text and not files:
        raise HTTPException(status_code=400, detail="Either text or image is mandatory to create a post")
    if files:
        for file in files:
            if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise HTTPException(status_code=422, detail="Invalid file type")
    
    post_crud.createPost(db, user_id=user.id, text = text, files=files)
    return {"detail": "Post Created"}


@router.get("/me/{post_id}", status_code=200, description = "To view a particular post by the current user")
async def readMyPost(
    post_id: int,
    user: UserModel = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
    ) -> PostResponse:
    if not user:
        raise HTTPException(401, detail = "Request needs user to be authorized")
    post = post_crud.readMyPost(db = db, post_id = post_id, user_id = user.id)
    if not post:
        raise HTTPException(404, "Post not found")
    return post


@router.get("/me", status_code=200, description = "To view all the posts posted by the current user")
async def readMyPosts(
    user: UserModel = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
    ) -> list[PostResponse]:
    if not user:
        raise HTTPException(401, detail = "Request needs user to be authorized")
    posts = post_crud.readMyPosts(db = db, user_id = user.id)
    if not posts:
        raise HTTPException(404, "No post found")
    return posts


@router.get("/{post_id}", status_code=200, description = "To view a particular public post")
async def readPost(
    post_id: int,
    user: UserModel = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
    ) -> PostResponse:
    if not user:
        raise HTTPException(401, detail = "Request needs user to be authorized")
    post = post_crud.readPost(db = db, post_id = post_id, user_id = user.id)
    if not post:
        raise HTTPException(404, "Post not found")
    if post.user_id == user.id:
        raise HTTPException(303, f'http://127.0.0.1:8000/posts/me/{post_id}')
    return post


@router.get("/", status_code=200, description = "To view all the public posts everyone has made. This also includes private post of the current user")
async def readPosts(
    user: UserModel = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
    ) -> list[PostResponse]:   
    posts = post_crud.readPosts(db = db, user_id = user.id)
    if not posts:
        raise HTTPException(404, "No post found")
    return posts


@router.patch("/{post_id}", status_code=204, description = "To update a post by the current user")
async def updatePost(
    post: PostUpdate = Depends(PostUpdate.init),
    db: Session = Depends(deps.get_db), 
    user: UserModel = Depends(deps.get_current_active_user),
    files: list[UploadFile] = File()
    ):
     
    if not user:
        raise HTTPException(401, detail = "Request needs user to be authorized")
    
    db_post = post_crud.getPostById(db, post_id = post.id, status_code = 1)

    if not db_post:
        raise HTTPException(404, detail = "Post not found")

    if db_post.user_id != user.id:
        raise HTTPException(401, detail = "Cannot update other's posts")
    
    post_crud.updatePost(db = db, post = post, db_post = db_post, files = files)
    return {"detail": "Post updated"}


@router.delete("/{post_id}", status_code=204, description = "To delete a post by the current user")
async def deletePost(
    post_id : int, 
    db: Session = Depends(deps.get_db), 
    user: UserModel = Depends(deps.get_current_active_user)
):
    if not user:
        raise HTTPException(401, "Request needs user to be authorized")
    post = post_crud.getPostById(db = db, post_id=post_id, status_code = 1)
    if not post:
        raise HTTPException(404, detail = "Post not found")
    if post.user_id !=  user.id:
        raise HTTPException(401, detail = "Can't delete other's posts") 
    post_crud.deletePost(db = db, post = post)
    return {"detail": "Post deleted"}