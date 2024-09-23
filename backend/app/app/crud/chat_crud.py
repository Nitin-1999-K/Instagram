from models import Chat as ChatModel
from sqlalchemy import desc, case, or_, func
from sqlalchemy.orm import Session


def sendMessage(db: Session, sender_id: int, receiver_id: int, message: str):
    chat = ChatModel(sender_id = sender_id, receiver_id = receiver_id, message = message)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def readChat(db: Session, person_id : int, friend_id: int):
    chats = db.query(ChatModel).filter(ChatModel.sender_id.in_([person_id, friend_id]), 
    ChatModel.receiver_id == case((ChatModel.sender_id == person_id, friend_id), else_ = person_id),
    ChatModel.status_code == 1).order_by(desc(ChatModel.created_datetime), desc(ChatModel.id)).all()
    return [chat for chat in chats]



def readChats(db: Session, person_id: int):

    friend_id = case((ChatModel.sender_id == person_id, ChatModel.receiver_id), (ChatModel.receiver_id == person_id, ChatModel.receiver_id))

    subquery = db.query(case((ChatModel.sender_id == person_id, ChatModel.receiver_id), (ChatModel.receiver_id == person_id, ChatModel.receiver_id)).label("friend_id"), 
    func.max(ChatModel.created_datetime).label('latest_chat_datetime'))\
    .filter(or_(ChatModel.sender_id == person_id, ChatModel.receiver_id == person_id), ChatModel.status_code == 1)\
    .group_by(friend_id).subquery()

    chats = db.query(ChatModel).join(subquery, (friend_id == subquery.c.friend_id) & 
    (ChatModel.created_datetime == subquery.c.latest_chat_datetime)).all()

    return chats



def getChatById(db: Session, chat_id: int):
    return db.query(ChatModel).filter(ChatModel.id == chat_id, ChatModel.status_code == 1).first()


def updateMessage(db: Session, chat: ChatModel, message: str):
    chat.message = message
    db.commit()
    db.refresh(chat)
    return chat
    

def deleteMessage(db: Session, chat: ChatModel):
    chat.status_code = -1
    db.commit()
    db.refresh(chat)
    return chat

# Delete one chat
# Deletee all chat
