from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv


class ConversationDatabase:

    _instance = None  #Singelton Instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConversationDatabase, cls).__new__(cls)
            cls._initialized = False
        return cls._instance
    
    def __init__(self):

        if self._initialized:
            return
        load_dotenv()
        self.database_url = os.getenv('DATABASE_URL')
        self.database_engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= self.database_engine)
        self.Base = declarative_base()
        self._initialized = True



    
