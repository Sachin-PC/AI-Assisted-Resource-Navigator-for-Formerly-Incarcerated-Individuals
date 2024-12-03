from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from src.ai_arnfi.config.configuration import SECRET_KEY, ALGORITHM,  DEFAULT_EXPIRE_DELTA_TIME_IN_MINUTES

def create_access_token(data:dict, expires_time: Optional[timedelta] = None):
    data_to_encode = data.copy()
    token_expiry_time = datetime.utcnow() + (expires_time if expires_time else timedelta(minutes=DEFAULT_EXPIRE_DELTA_TIME_IN_MINUTES))
    data_to_encode.update({"exp":token_expiry_time})
    access_token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token 