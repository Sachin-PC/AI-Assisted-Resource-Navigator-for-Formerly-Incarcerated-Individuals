
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableMap
from sqlalchemy.orm import Session
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage

import logging
import src.ai_arnfi.components.conversational_db.schemas as schemas
import src.ai_arnfi.components.retriever.chainedRetreiver as chainedRetreiver
from src.ai_arnfi.components.conversational_db.models import User, ChatSession, Message
from src.ai_arnfi.components.conversational_db.chatMessageHistory import ListChatMessageHistory
import src.ai_arnfi.components.conversational_db.db_operations as db_operations
import src.ai_arnfi.config.configuration as config



class EvaluationConversationalChain:
    def __init__(self):
        self.model_name = config.MODEL_NAME
        self.chat_gpt_model = ChatOpenAI(model=self.model_name, temperature=config.MODEL_TEMPERATURE)
        self.last_k_conversations = 6
        self.SYS_PROMPT = """Act as a helpful assistant and give brief answers"""
        self.llmchain = None
        self.conversational_chain = None
        self.database_parameters_config = None
        self.humanMessageType = "HumanMessage"
        self.aIMessageType = "AIMessage" 
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.SYS_PROMPT),
                MessagesPlaceholder(variable_name="history"),
                MessagesPlaceholder(variable_name="retrieved_documents"),
                ("human","{query}"),
            ]
        )
        self.create_conversational_chain()
    
    # def get_converstaion_history(self, database_session:Session, user_id:int, chat_session_id:int, last_k_conversations:int = 10):
    #     messages = db_operations.get_message_history(database_session, user_id,chat_session_id,last_k)
    #     conversation_history = []
    #     for message in history:
    #         conversation_history.append({
    #             "role":message.message_type,
    #             "content": message.content
    #             })
    #     # print("history = \n",conversation_history,"\n\n\n")
    #     # return conversation_history
    #     print("history = ",history)
    #     return conversation_history

    def get_converstaion_history(self, input_data):
        database_session = input_data['database_session']
        user_id = input_data['user_id']
        chat_session_id = input_data['chat_session_id']
        last_k_conversations= input_data['last_k_conversations']
        print("----------------------")
        print(f"user_id = {user_id}")

        messages = db_operations.get_message_history(database_session, user_id,chat_session_id,last_k_conversations)
        conversation_history = []
        for message in messages:
            conversation_history.append(self._transform_to_base_message(message))
        print("conversation_history = ",conversation_history)
        return conversation_history

    def _transform_to_base_message(self,message) -> BaseMessage:
        if message.message_type == self.humanMessageType:
            return HumanMessage(content=message.content)
        elif message.message_type == self.aIMessageType:
            return AIMessage(content=message.content)
        else:
            raise ValueError(f"Unknown Message Type: {message.type}")

    def save_response(self, input_data, ai_response):
        database_session = input_data['database_session']
        user_id = input_data['user_id']
        chat_session_id = input_data['chat_session_id']
        last_k_conversations= input_data['last_k_conversations']
        query = input_data['query']
        userQueryMessage = schemas.CreateMessage(message_type=self.humanMessageType,content=query)
        aiResponseMessage = schemas.CreateMessage(message_type=self.aIMessageType,content=ai_response)
        # messagesToAdd = [userQueryMessage,aiResponseMessage ]
        # db_operations.add_messages(database_session, chat_session_id, messagesToAdd)
        db_operations.add_message(database_session, chat_session_id, userQueryMessage)
        db_operations.add_message(database_session, chat_session_id, aiResponseMessage)
        # print("input_data = ",input_data)

    
    def create_conversational_chain(self):

        self.llmchain = (
            RunnableMap({
                'history': RunnableLambda(self.get_converstaion_history),
                'query': lambda x: x['query'],
                'retrieved_documents': RunnableLambda(self.retrieve_documents),
            })
            |
            RunnableLambda(self.debug_prompt_output) 
            |
            RunnableMap({
                "prompt": self.prompt,
                "retrieved_documents": lambda x: x["retrieved_documents"]
            })
            |
            RunnableLambda(self.debug_prompt_output) 
            |
            RunnableMap({
                "response": lambda x: self.chat_gpt_model.invoke(x["prompt"]),
                "retrieved_documents": lambda x: x["retrieved_documents"]
            })
            |
            RunnableLambda(self.debug_prompt_output) 
        )
        
    def debug_prompt_output(self, input_data):
        print("\n--- Debugging Prompt Output ---")
        print(input_data)
        print("--- End of Debug ---\n")
        return input_data  # Pass the data to the next step in the chain
        
    def get_response_from_llm(self, prompt: str, user_id: int, chat_session_id: int, database_session: Session):
        
        # print("INSIDE")
        input_data = {
            "query": prompt,
            "database_session": database_session,
            "user_id": user_id,
            "chat_session_id": chat_session_id,
            "last_k_conversations": self.last_k_conversations,
        }
        # config_data = {
        #     "database_session": database_session,
        #     "user_id": user_id,
        #     "chat_session_id": chat_session_id,
        #     "last_k_conversations": last_k_conversations,
        # }

        aiResponse = ""
        for chunk in self.llmchain.stream(input_data):
            print(chunk.content, end="")
            aiResponse += chunk.content

        print("aiResponse = ",aiResponse)
        self.save_response(input_data,aiResponse)
        return aiResponse

    def retrieve_documents(self, input_data):

        query = input_data["query"]
        
        similarity_retriever_config = {
            "similarity_retriever_search_type": config.SIMILARITY_RETRIEVER_SEARCH_TYPE,
            "similarity_retriever_similarity_k": config.SIMILARITY_RETRIEVER_SIMILARITY_K
        }
        chianed_retriever_model = chainedRetreiver.get_chained_retreiver(similarity_retriever_config)
        retrieved_documents = chianed_retriever_model.invoke(query)
        print("\n\nretrieved_documents = \n\n",retrieved_documents)
        ret_docs = []
        for document in retrieved_documents:
            ret_docs.append(HumanMessage(content=document.page_content))
        print("\n\nret_docs:\n\n",ret_docs)
        return ret_docs
    
    
    def get_response_and_context_from_llm(self, prompt: str, user_id: int, chat_session_id: int, database_session: Session):
        
        # print("INSIDE")
        input_data = {
            "query": prompt,
            "database_session": database_session,
            "user_id": user_id,
            "chat_session_id": chat_session_id,
            "last_k_conversations": self.last_k_conversations,
        }
        # config_data = {
        #     "database_session": database_session,
        #     "user_id": user_id,
        #     "chat_session_id": chat_session_id,
        #     "last_k_conversations": last_k_conversations,
        # }

        response = self.llmchain.invoke(input_data)
        print(response)
        # aiResponse = ""
        # for chunk in self.llmchain.stream(input_data):
        #     print(chunk.content, end="")
        #     aiResponse += chunk.content

        # print("aiResponse = ",aiResponse)
        # self.save_response(input_data,aiResponse)
        # return aiResponse