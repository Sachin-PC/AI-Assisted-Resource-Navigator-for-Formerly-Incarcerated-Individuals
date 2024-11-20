from passlib.context import CryptContext


crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return crypto_context.hash(password)