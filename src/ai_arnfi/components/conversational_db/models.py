from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from  src.ai_arnfi.components.conversational_db.database import ConversationDatabase

conversationDatabase = ConversationDatabase()
Base = conversationDatabase.Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index = True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    chat_sessions = relationship('ChatSession', back_populates='user')

class ChatSession(Base):
    __tablename__ = 'chat_sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    chat_session_name = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship('User', back_populates='chat_sessions')
    messages = relationship('Message', back_populates='chat_session')

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    chat_session_id = Column(Integer, ForeignKey('chat_sessions.id'), nullable=False)
    message_type = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    chat_session = relationship('ChatSession', back_populates='messages')
