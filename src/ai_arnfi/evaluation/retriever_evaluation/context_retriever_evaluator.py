from llama_index.core.llama_pack import download_llama_pack
import pandas as pd
import src.ai_arnfi.config.configuration as configuration
from dotenv import load_dotenv
from langchain.callbacks.tracers import LangChainTracer
from langsmith import client
from langsmith.evaluation import evaluate
from langsmith import Client
from  src.ai_arnfi.components.conversational_db import models
from src.ai_arnfi.components.evaluation_conversational_chan import EvaluationConversationalChain
from langsmith.evaluation import LangChainStringEvaluator, evaluate

class ContextRetrieverEvaluator:
    def __init__(self):
        load_dotenv()
        self.client = Client(timeout_ms=3600000)
        self.conversationDatabase = models.ConversationDatabase()
        self.Base = self.conversationDatabase.Base
        self.Base.metadata.create_all(bind=self.conversationDatabase.database_engine)
        self.conversationDatabaseSession = self.conversationDatabase.SessionLocal()
        self.evaluation_conversational_chan = EvaluationConversationalChain()

    def evaluate_response(self):
        user_id = 1
        chat_session_id = 1
        # query = "Who did the ACLU represent in the case and what were the allegations made against the Department of Commerce's decision to add a citizenship question to the 2020 census?"
        query = "Explain how state laws can vary in different areas such as divorce, DUI, estate planning, and medical malpractice. Provide examples from any two states."
        self.evaluation_conversational_chan.get_response_and_context_from_llm(query,user_id, chat_session_id, self.conversationDatabaseSession)

        
contextRetrieverEvaluator = ContextRetrieverEvaluator()
contextRetrieverEvaluator.evaluate_response()