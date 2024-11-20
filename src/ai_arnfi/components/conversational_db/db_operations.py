from sqlalchemy.orm import Session
from src.ai_arnfi.components.conversational_db.models import User, ChatSession, Message
from typing import List
import src.ai_arnfi.components.conversational_db.schemas as schemas
import src.ai_arnfi.components.conversational_db.authorization as authorization
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

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
    
def create_session(database: Session, user_id: int, chat_session_name: str = None):
    try:
        new_user_chat_session = ChatSession(user_id=user_id, chat_session_name =chat_session_name)
        database.add(new_user_chat_session)
        database.commit()
        database.refresh(new_user_chat_session)
        return new_user_chat_session
    except:
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
    except:
        database.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occured while creating a chat session for the user. Error reason: {str(e)}"
        )
    
def get_message_history(database:Session, user_id:int, chat_session_id:int) -> List[Message]:

    valid_session = database.query(ChatSession).filter(
        ChatSession.id == chat_session_id,
        ChatSession.user_id == user_id
    ).first()
    if not valid_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Chat Session or User Id"
        )
    
    messages = database.query(Message).filter(
        Message.chat_session_id == chat_session_id
    ).order_by(
        Message.timestamp.desc()
    ).all()

    return messages





