
from langchain_community.document_loaders import UnstructuredHTMLLoader
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
import src.ai_arnfi.config.configuration as config
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import src.ai_arnfi.components.conversational_db.db_operations as db_operations

class ConversationalChain:
    def __init__(self):
        self.model_name = config.MODEL_NAME
        self.chat_gpt_model = ChatOpenAI(model=self.model_name, temperature=config.MODEL_TEMPERATURE)
        self.SYS_PROMPT = """Act as a helpful assistant and give brief answers"""
        self.conversational_chain = None
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.SYS_PROMPT),
                MessagesPlaceholder(variable_name="history"),
                ("human","{query}"),
            ]
        )

    def get_converstaion_history(user_id, session_id):
        db_operations.get_message_history(user_id=user_id,session_id=session_id)
        # messages = None
        return []
    
    def get_last_k_messages_history(messages, k=2):
        return messages[-(k+1):]
    
    def create_chain(self):
        self.conversational_chain = (
            RunnablePassthrough(
                history = RunnableLambda(self.get_last_k_messages_history)
            )
            |
            self.prompt
            |
            self.chat_gpt_model
        )
        
    def add_data(self,documents,ids):
        self.chroma_database.add_documents(documents=documents, ids=ids)

    def get_data(self):
        return self.chroma_database.get(include=['embeddings', 'documents', 'metadatas','uris'])









    