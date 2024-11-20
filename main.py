from ai_arnfi.components.conversational_db import db_operations as conversationDatabase_crud
from  src.ai_arnfi.components.conversational_db import models, schemas

conversationDatabase = models.ConversationDatabase()
Base = conversationDatabase.Base
# Base.metadata.create_all(bind=conversationDatabase.database_engine)

conversationDatabaseSession = conversationDatabase.SessionLocal()

# new_user = schemas.CreateUser(username="Sachin", password="Sachin")
# res = conversationDatabase_crud.create_user(conversationDatabaseSession,new_user)


# new_chat_session = schemas.CreateSession(session_name="Chat1")
#  user_id: int, chat_session_name: str = None
# res = conversationDatabase_crud.create_session(conversationDatabaseSession,1,"chat_1")


new_message = schemas.CreateMessage(message_type="Human",content="This is a test message")
# res = conversationDatabase_crud.add_message(conversationDatabaseSession,1,new_message)


messages = conversationDatabase_crud.get_message_history(conversationDatabaseSession, 1, 1)
print(messages[0].message_type)
print(messages[0].content)
