from src.ai_arnfi.components.conversational_chain import ConversationalChain
from  src.ai_arnfi.components.conversational_db import models
from sqlalchemy.orm import Session


class UserChatService:
    def __init__(self):
        self.conversational_chain = ConversationalChain()

    def get_response(self,  database_session: Session, user_query: str, user_id: int, chat_session_id: int):
        response = self.conversational_chain.get_response_from_llm(user_query,user_id, chat_session_id, database_session)

        return response

