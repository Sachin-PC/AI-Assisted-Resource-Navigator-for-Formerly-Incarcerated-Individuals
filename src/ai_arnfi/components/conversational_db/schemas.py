from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CreateUser(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description="Username cannot be empty")
    password: str = Field(..., min_length=1, max_length=50, description="Password cannot be empty")

class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CreateSession(BaseModel):
    session_name: Optional[str]
    

class Session(BaseModel):
    id: int
    session_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class CreateMessage(BaseModel):
    content: str
    message_type: str

class Message(BaseModel):
    id: int
    message_type: str
    content: str
    timestamp: datetime


    class Config:
        from_attributes = True

