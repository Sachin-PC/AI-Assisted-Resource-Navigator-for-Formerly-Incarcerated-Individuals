
from langchain_community.document_loaders import UnstructuredHTMLLoader
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

class VectorDatabase:
    def __init__(self):
        # self.data_directory = "/Users/sachinpc/Documents/GitHubProjects/AI_FOR_HCI/Crawled Data/1000/data/succesful_requests/"
        self.vector_db_directory = "/Users/sachinpc/Documents/GitHubProjects/AI_FOR_HCI/AI-Assisted-Resource-Navigator-for-Formerly-Incarcerated-Individuals/database/vector_database/chroma_db"
        self.hf_embeddings = HuggingFaceEmbeddings(
            model_name="mixedbread-ai/mxbai-embed-large-v1",
        )

        self.chroma_database = Chroma(collection_name='legal_data_documents',
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








    