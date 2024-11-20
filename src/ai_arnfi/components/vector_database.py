
from langchain_community.document_loaders import UnstructuredHTMLLoader
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import src.ai_arnfi.config.configuration as configuration

class VectorDatabase:
    def __init__(self):
        self.vector_db_directory = configuration.VECTOR_DB_DIRECTORY
        self.hf_embeddings = HuggingFaceEmbeddings(
            model_name=configuration.EMBEDDING_MODEL_NAME,
        )

        self.chroma_database = Chroma(collection_name=configuration.VECTOR_DB_COLLECTION_NAME,
                                 embedding_function=self.hf_embeddings,
                                 persist_directory=self.vector_db_directory
                                 )
        
    def add_data(self,documents,ids):
        self.chroma_database.add_documents(documents=documents, ids=ids)

    def get_data(self):
        return self.chroma_database.get(include=['embeddings', 'documents', 'metadatas','uris'])


vectorDatabase = VectorDatabase()
data = vectorDatabase.get_data()
print(data)
# documents = [ 'ABCDEFGHIJKLMNOOPQRS',
#  'Music therapy can aid in the mental well-being of individuals.',
#  'The Milky Way is just one of billions of galaxies in the universe.',
#  'Economic theories help understand the distribution of resources in society.',
#  'Yoga is an ancient practice that involves physical postures and meditation.']

# ids = ['doc_'+str(i) for i in range(len(documents))]
# ids

# vectorDatabase.add_data(documents,ids)
# data = vectorDatabase.get_data()
# print(data)

# new_ids = ['doc_'+str(i+len(ids)) for i in range(len(new_documents))]
# new_ids








    