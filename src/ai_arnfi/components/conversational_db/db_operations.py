from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.ai_arnfi.components.conversational_db.models import User, ChatSession, Message
import src.ai_arnfi.components.conversational_db.schemas as schemas
import src.ai_arnfi.components.conversational_db.authorization as authorization


def create_user(database: Session, user: schemas.CreateUser):

    try:
        hashed_password = authorization.get_password_hash(user.password)
        new_user = User(username=user.username, hashed_password=hashed_password)
        database.add(new_user)
        database.commit()
        database.refresh(new_user)
        return new_user
    except IntegrityError as e:
        database.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"\n\n\n\n\n\nUsername already exists. Please choose a different username. Error reason: {str(e)}"
        )

    except Exception as e:
        database.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occured while creating the user. Error reason: {str(e)}"
        )
    
def create_chat_session(database: Session, user_id: int, chat_session_name: str = None):
    try:
        new_user_chat_session = ChatSession(user_id=user_id, chat_session_name =chat_session_name)
        database.add(new_user_chat_session)
        database.commit()
        database.refresh(new_user_chat_session)
        return new_user_chat_session
    except Exception as e:
        database.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occured while creating a chat session for the user. Error reason: {str(e)}"
        )
    

def add_message(database: Session, chat_session_id:int, message_details: schemas.CreateMessage):
    try:
        new_message = Message(chat_session_id=chat_session_id, message_type=message_details.message_type, content=message_details.content)
        database.add(new_message)
        database.commit()
        database.refresh(new_message)
        return new_message
    except Exception as e:
        database.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occured while creating a chat session for the user. Error reason: {str(e)}"
        )

def add_messages(database: Session, chat_session_id:int, messages_infomration:List[schemas.CreateMessage]):
    try:
        new_messages = []
        for message_infomration in messages_infomration:
            new_message = Message(chat_session_id = chat_session_id, message_type=message_infomration.message_type, content=message_infomration.content)
            database.add(new_message)
            new_messages.append(new_message)
        database.commit()
        for new_message in new_messages:
            database.refresh(new_message)
    except Exception as e:
        database.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occured while creating a chat session for the user. Error reason: {str(e)}"
        )
    return
    
def get_message_history(database_session:Session, user_id:int, chat_session_id:int, last_k_conversations:int = 10) -> List[Message]:

    print("-------------------------------------")
    print("database_session = ",database_session)
    print("user_id = ",user_id)
    print("chat_session_id = ",chat_session_id)
    print("last_k_conversations = ",last_k_conversations)
    print("-------------------------------------")

    valid_session = database_session.query(ChatSession).filter(
        ChatSession.id == chat_session_id,
        ChatSession.user_id == user_id
    ).first()
    if not valid_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Chat Session or User Id"
        )
    
    messages = database_session.query(Message).filter(
        Message.chat_session_id == chat_session_id
    ).order_by(
        Message.timestamp.desc()
    ).limit(last_k_conversations).all()

    return messages[::-1]

def get_user_by_user_id(database_session:Session, user_id:int):
    try:
        user = database_session.query(User).filter(
                    User.id == user_id
                ).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid User details. User not found"
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occured while getting the user details. Error reason: {str(e)}"
        )

def get_user_by_username(database_session:Session, username:str):
    try:
        user = database_session.query(User).filter(
                    User.username == username
                ).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid User details. User not found"
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occured while getting the user details. Error reason: {str(e)}"
        )






