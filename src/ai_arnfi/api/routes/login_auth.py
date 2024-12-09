from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel
import src.ai_arnfi.components.conversational_db.db_operations as db_operations
from src.ai_arnfi.components.conversational_db.authorization import verify_password
from src.ai_arnfi.config.configuration import ACCESS_TOKEN_EXPIRE_MINUTES
from src.ai_arnfi.utils.security import create_access_token
from src.ai_arnfi.api.dependencies import get_database_session
import src.ai_arnfi.components.conversational_db.schemas as schemas


from src.ai_arnfi.components.conversational_db.schemas import Token 

login_router = APIRouter()

class LoginData(BaseModel):
    username: str
    password: str

@login_router.post("/login", response_model=Token)
def user_login(
        user_data: LoginData,
        database_session: Session = Depends(get_database_session)
        # user_data: OAuth2PasswordRequestForm = Depends()
    ):
    user = db_operations.get_user_by_username(database_session, user_data.username)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password"
        )
    access_token_expiry_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_time = access_token_expiry_time
    )
    
    return {"access_token": access_token, "token_type":"bearer"}


@login_router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(
        user: schemas.CreateUser,
        database_session: Session = Depends(get_database_session),
    ):
    try:
        user = db_operations.create_user(database_session, user)
        return user
    except Exception as e:
        print(f'Caught exception: {e}')
        raise
    
