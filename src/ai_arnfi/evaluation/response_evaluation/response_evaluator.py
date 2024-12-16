from llama_index.core.llama_pack import download_llama_pack
import pandas as pd
import src.ai_arnfi.config.configuration as configuration
from dotenv import load_dotenv
from langchain.callbacks.tracers import LangChainTracer
from langsmith import client
from langsmith.evaluation import evaluate
from langsmith import Client
from  src.ai_arnfi.components.conversational_db import models
from src.ai_arnfi.components.conversational_chain import ConversationalChain
from langsmith.evaluation import LangChainStringEvaluator, evaluate

class ResponseEvaluator:
    def __init__(self):
        load_dotenv()
        self.client = Client(timeout_ms=3600000)
        self.conversationDatabase = models.ConversationDatabase()
        self.Base = self.conversationDatabase.Base
        self.Base.metadata.create_all(bind=self.conversationDatabase.database_engine)
        self.conversationDatabaseSession = self.conversationDatabase.SessionLocal()
        self.conversational_chain = ConversationalChain()
        
        self.qa_evaluator = LangChainStringEvaluator("qa")
        self.correct_evaluator = LangChainStringEvaluator("labeled_criteria",
                                             config={ "criteria": "correctness"})
        self.conciseness_evaluator =LangChainStringEvaluator("criteria",
                                                        config={ "criteria": "conciseness"})
        self.helpfulness_evaluator = LangChainStringEvaluator("criteria",
                                                        config={ "criteria": "helpfulness"})
        self.semantic_evaluator = LangChainStringEvaluator("embedding_distance")

    def evaluate_response(self):
        user_id = 17
        chat_session_id = 42
        results = evaluate(
            lambda x: self.conversational_chain.get_response_from_llm(x['question'],user_id, chat_session_id, self.conversationDatabaseSession),
            client = self.client,
            data = "Sample Evaluation Test - AARNFI ET003(SmallDataset_size_5)",
            experiment_prefix="test_eval001",
            evaluators=[self.correct_evaluator, self.conciseness_evaluator, self.helpfulness_evaluator, self.semantic_evaluator]
        )
        # self.conversational_chain.get_response_from_llm(user_query,user_id, chat_session_id, self.conversationDatabaseSession)
        
        
response_evaluator = ResponseEvaluator()
response_evaluator.evaluate_response()