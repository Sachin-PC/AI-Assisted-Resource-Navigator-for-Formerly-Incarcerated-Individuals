
from langchain_community.document_loaders import UnstructuredHTMLLoader
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
import ai_arnfi.config.configuration as config
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class chatDatabase:
    def __init__(self):
        self.databaseEngine = None
        self.databaseName = None
        
    def createDatabase(self,databaseName):
        self.databaseEngine = create_engine(f"sqlite:///{databaseName}.db")
        self.databaseName = databaseName

    def getDatabase(self):
        Session = sessionmaker(bind=self.databaseEngine)
        session = Session()