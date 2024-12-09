from fastapi import APIRouter, Depends, HTTPException, status
from src.ai_arnfi.components.conversational_db.schemas import UserQueryRequest, QueryResponse, ChatSession
from src.ai_arnfi.services.user_chat_service import UserChatService
from sqlalchemy.orm import Session
from src.ai_arnfi.api.dependencies import get_database_session, get_user
from src.ai_arnfi.components.conversational_db import db_operations

conversation_router = APIRouter()

def get_user_chat_service():
    print("NNNNNNNNNNNNNNNNNNN")
    return UserChatService()

@conversation_router.post("/legalchat/{chat_id}/get_response", response_model=QueryResponse)
async def get_repsonse_endpoint(
    chat_id: int,
    userQueryRequest: UserQueryRequest,
    userChatService : UserChatService = Depends(get_user_chat_service),
    database_session: Session = Depends(get_database_session),
    current_user : UserChatService = Depends(get_user)
):
    try:
        user_query = userQueryRequest.user_query
        user_id = current_user.id
        chat_session_id = chat_id
        result = userChatService.get_response(database_session, user_query, user_id, chat_session_id)
        return QueryResponse(user_query_response=result, chat_session_id=chat_session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@conversation_router.post("/legalchat/get_response", response_model=QueryResponse)
async def create_session_and_get_response(
    userQueryRequest: UserQueryRequest,
    userChatService : UserChatService = Depends(get_user_chat_service),
    database_session: Session = Depends(get_database_session),
    current_user : UserChatService = Depends(get_user)
):
    try:
        user_query = userQueryRequest.user_query
        user_id = current_user.id
        # chat_session_id = chat_id
        user_new_chat_session = db_operations.create_chat_session(database_session,current_user.id)
        chat_session_id = user_new_chat_session.id
        result = userChatService.get_response(database_session, user_query, user_id, chat_session_id)
        return QueryResponse(user_query_response=result, chat_session_id=chat_session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@conversation_router.post("/create_user_chat_session", response_model=ChatSession)
async def get_repsonse_endpoint(
    database_session: Session = Depends(get_database_session),
    current_user : UserChatService = Depends(get_user)
):
    try:
        user_new_chat_session = db_operations.create_chat_session(database_session,current_user.id)
        return user_new_chat_session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# user_query = "What are legal documents?"
# user_id = 1
# chat_session_id = 1
# userChatService = UserChatService()
# response = userChatService.get_response(user_query, user_id, chat_session_id)