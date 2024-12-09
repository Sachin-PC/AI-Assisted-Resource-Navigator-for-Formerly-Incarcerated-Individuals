from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.ai_arnfi.config.configuration import SECRET_KEY, ALGORITHM
from  src.ai_arnfi.components.conversational_db import models
from src.ai_arnfi.components.conversational_db.db_operations import get_user_by_user_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def get_database_session():
    conversationDatabase = models.ConversationDatabase()
    Base = conversationDatabase.Base
    Base.metadata.create_all(bind=conversationDatabase.database_engine)
    conversationDatabaseSession = conversationDatabase.SessionLocal()
    return conversationDatabaseSession

def get_user(
    database_session:Session = Depends(get_database_session),
    access_token: str = Depends(oauth2_scheme)
):
    print("\n\naccess token = ",access_token)
    try:
        data = jwt.decode(access_token,SECRET_KEY, ALGORITHM)
        user_id: str = data.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid Credentials"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Credentials"
        )
    try:
        user = get_user_by_user_id(database_session, user_id = int(user_id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid Credentials"
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occured while getting the user details. Error reason: {str(e)}"
        ) 
    