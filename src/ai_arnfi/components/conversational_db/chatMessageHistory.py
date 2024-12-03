from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from typing import List
from sqlalchemy.orm import Session

from src.ai_arnfi.components.conversational_db.models import Message

class ListChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, messages:List[Message], database_session:Session, user_id:int, chat_session_id:int):
        self.database_session = database_session
        self.user_id = user_id
        self.chat_session_id = chat_session_id
        self.humanMessageType = "HumanMessage"
        self.aIMessageType = "AIMessage"
        self.messages = [
            self._transform_to_base_message(message) for message in messages
        ]

    def _transform_to_base_message(self,message) -> BaseMessage:
        if message.message_type == self.humanMessageType:
            return HumanMessage(content=message.content)
        elif message.message_type == self.aIMessageType:
            return AIMessage(content=message.content)
        else:
            raise ValueError(f"Unknown Message Type: {message.type}")

    def clear(self) -> None:
        # Clear the internal list if needed
        self.messages = []

    def add_message(self, message: BaseMessage) -> None:
        if instance(message, HumanMessage):
            newMessage = schemas.CreateMessage(message_type=humanMessageType,content=message.content)
        elif instance(message, AIMessage):
            newMessage = schemas.CreateMessage(message_type=aIMessageType,content=message.content)
        else:
            raise ValueError(f"Unsupported Message type: {type(message)}")

        res = add_message(self.database_session, self.chat_session_id, newMessage)
        print("res = ",res)