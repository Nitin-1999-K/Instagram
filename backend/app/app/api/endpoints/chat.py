from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from api.deps import get_db
from crud import chat_crud
from api import deps
from models import User as UserModel
from schemas import ChatResponse

router = APIRouter(prefix="/chats")

@router.post("/")
def createChat(
    receiver_id: int,
    message: str = Body(),
    db: Session = Depends(deps.get_db),
    user: UserModel = Depends(deps.get_current_active_user)
):
    if not user:
        raise HTTPException(404, "User not found")
    # receiver = if not receiver raise 
    return chat_crud.sendMessage(db = db, sender_id = user.id, receiver_id = receiver_id, message = message)


@router.get("/{friend_id}")
def readChat(
    friend_id: int,
    user: UserModel = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)) -> list[ChatResponse]:
    if not user:
        raise HTTPException(status_code=401, detail = "Request needs user to be authenticated")
    return chat_crud.readChat(db = db, person_id=user.id, friend_id= friend_id)


@router.get("/")
def readChats(
    user: UserModel = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)) -> list[ChatResponse]:
    if not user:
        raise HTTPException(status_code=401, detail = "Request needs user to be authenticated")
    return chat_crud.readChats(db = db, person_id = user.id)


@router.patch("/{chat_id}")
def updateMessage(
    chat_id: int,
    message: str = Body(),
    user: UserModel = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)):
    if not user:
        raise HTTPException(status_code=401, detail = "Request needs user to be authenticated")
    chat = chat_crud.getChatById(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail = "Message not found")
    if not chat.sender_id == user.id:
        raise HTTPException(status_code=401, detail="Can't update other's messages")
    chat = chat_crud.updateMessage(db = db, message = message, chat = chat)
    return chat


@router.delete("/{chat_id}")
def deleteMessage(
    chat_id: int,
    user: UserModel = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)):
    if not user:
        raise HTTPException(status_code=401, detail = "Request needs user to be authenticated")
    chat = chat_crud.getChatById(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail = "Message not found")
    if not chat.sender_id == user.id:
        raise HTTPException(status_code=401, detail="Can't delete other's messages")
    chat = chat_crud.deleteMessage(db = db, chat = chat)
    return chat