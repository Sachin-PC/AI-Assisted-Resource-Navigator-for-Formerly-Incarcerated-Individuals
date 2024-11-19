
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

class ConversationalChain:
    def __init__(self):
        self.model_name = config.MODEL_NAME
        self.chat_gpt_model = ChatOpenAI(model=self.model_name, temperature=config.MODEL_TEMPERATURE)

        



        
    def add_data(self,documents,ids):
        self.chroma_database.add_documents(documents=documents, ids=ids)

    def get_data(self):
        return self.chroma_database.get(include=['embeddings', 'documents', 'metadatas','uris'])









    