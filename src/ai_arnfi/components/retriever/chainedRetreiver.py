from langchain_openai import ChatOpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.document_compressors import CrossEncoderReranker
from dotenv import load_dotenv

from src.ai_arnfi.components.vector_database import VectorDatabase
import src.ai_arnfi.config.configuration as configuration



def get_chained_retreiver(similarity_retriever_config:dict):
    load_dotenv()
    similarity_retreiver_search_type = similarity_retriever_config['similarity_retriever_search_type']
    similarity_retreiver_similarity_k = similarity_retriever_config['similarity_retriever_similarity_k']
    search_kwargs = {"k":similarity_retreiver_similarity_k}

    vector_database = VectorDatabase()
    similarity_retriever = vector_database.get_similarity_retriever(similarity_retreiver_search_type, search_kwargs)

    model_name = configuration.MODEL_NAME
    chat_gpt_model = ChatOpenAI(model=model_name, temperature=configuration.MODEL_TEMPERATURE)
    llm_filter = LLMChainFilter.from_llm(llm = chat_gpt_model)

    compressor_retriever = ContextualCompressionRetriever(
        base_compressor=llm_filter, base_retriever=similarity_retriever
    )   

    reranker_model = HuggingFaceCrossEncoder(model_name=configuration.RERANKER_MODEL_NAME)
    reranker_compressor = CrossEncoderReranker(model=reranker_model, top_n=configuration.TOP_N)
    final_chianed_retriever_model = ContextualCompressionRetriever(
        base_compressor=reranker_compressor, base_retriever=compressor_retriever
    )

    return final_chianed_retriever_model



# config = {
#     "similarity_retriever_search_type": "similarity",
#     "similarity_retriever_similarity_k": 5
# }


# final_chianed_retriever_model = get_chained_retreiver(config)
# print(final_chianed_retriever_model.invoke("What are the legal documents for formerly incarcerated people"))