# from src.ai_arnfi.components.conversational_db import db_operations as conversationDatabase_crud
# from  src.ai_arnfi.components.conversational_db import models, schemas
# from src.ai_arnfi.components.conversational_chain import ConversationalChain

# # new_user = schemas.CreateUser(username="Sachin", password="Sachin")
# # res = conversationDatabase_crud.create_user(conversationDatabaseSession,new_user)


# # new_chat_session = schemas.CreateSession(session_name="Chat1")
# #  user_id: int, chat_session_name: str = None
# # res = conversationDatabase_crud.create_session(conversationDatabaseSession,1,"chat_1")

# # humanMessageType = "HumanMessage"
# # AIMessageType = "AIMessage"

# # message1 = schemas.CreateMessage(message_type=humanMessageType,content="This is the First Human Message")
# # message2 = schemas.CreateMessage(message_type=AIMessageType,content="This is the First AI Message")
# # message3 = schemas.CreateMessage(message_type=humanMessageType,content="This is the Second Human Message")
# # message4 = schemas.CreateMessage(message_type=AIMessageType,content="This is the Second AI Message")
# # message5 = schemas.CreateMessage(message_type=humanMessageType,content="This is the third Human Message")
# # message6 = schemas.CreateMessage(message_type=AIMessageType,content="This is the third AI Message")
# # res = conversationDatabase_crud.add_message(conversationDatabaseSession,1,new_message)


# # messages = conversationDatabase_crud.get_message_history(conversationDatabaseSession, 1, 1)
# # print(messages[0].message_type)
# # print(messages[0].content)

# # conversationDatabase_crud.add_message(conversationDatabaseSession,1,message1)
# # conversationDatabase_crud.add_message(conversationDatabaseSession,1,message2)
# # conversationDatabase_crud.add_message(conversationDatabaseSession,1,message3)
# # conversationDatabase_crud.add_message(conversationDatabaseSession,1,message4)
# # conversationDatabase_crud.add_message(conversationDatabaseSession,1,message5)
# # conversationDatabase_crud.add_message(conversationDatabaseSession,1,message6)

# # new_message = schemas.CreateMessage(message_type="AI",content="This is a test message")

# # conversationalChain = ConversationalChain()

# # history = conversationalChain.get_converstaion_history(conversationDatabaseSession,1, 1,100)


    
# # print(history)

# def main():
#     conversationDatabase = models.ConversationDatabase()
#     Base = conversationDatabase.Base
#     # Base.metadata.create_all(bind=conversationDatabase.database_engine)

#     conversationDatabaseSession = conversationDatabase.SessionLocal()
#     prompt ="What is AI"
#     user_id = 1
#     chat_session_id = 1
#     database_session = conversationDatabaseSession
#     last_k_conversations = 10
#     conversationalChain = ConversationalChain()
#     conversationalChain.get_response_from_llm( prompt,user_id, chat_session_id, database_session)


# main()



from fastapi import FastAPI
from src.ai_arnfi.api.routes.conversation_endpoints import conversation_router
from src.ai_arnfi.api.routes.login_auth import login_router
from src.ai_arnfi.services.user_chat_service import UserChatService
from fastapi import FastAPI

app = FastAPI(
    title="AI-ASSISTED-RESOURCE-NAVIGATOR-FOR-FORMERLEY-INCARCERATED",
    version="1.0.0"
)

login_router

app.include_router(conversation_router, prefix="/api")
app.include_router(login_router, prefix="/api/auth")

if  __name__ == "__main__":
    
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    
    uvicorn


# user_query = "What are legal documents?"
# user_id = 1
# chat_session_id = 1
# userChatService = UserChatService()
# response = userChatService.get_response(user_query, user_id, chat_session_id)