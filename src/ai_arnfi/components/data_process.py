from queue import PriorityQueue
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from  src.ai_arnfi.components.vector_database import VectorDatabase
import src.ai_arnfi.config.configuration as configuration

class DataProcess:
    def __init__(self):
        self.loaders = {
            '.html': (UnstructuredHTMLLoader, {})
        }
        self.data_directory = configuration.DATA_DIRECTORY
        self.batch_size = 2
        self.hf_embeddings = HuggingFaceEmbeddings(
            model_name=configuration.EMBEDDING_MODEL_NAME,
        )
        self.docs_processed_till_now = 0
        self.vectorDatabase = VectorDatabase()

    def batch_generator(self,iterable, batch_size):
        batch = []
        print("iterable = ",type(iterable))
        count = 0
        for item in iterable:
            print(type(item))
            print(item.metadata)
            count += 1
            print("count = ",count)
            batch.append(item)
            if len(batch) == batch_size:
                yield batch
                batch = []
            
        if batch:
            yield batch
    
    def create_directory_loader(self,file_type, directory_path):
        return DirectoryLoader(
            path = directory_path,
            glob=f'**/*{file_type}',
            loader_cls = self.loaders[file_type][0],
            loader_kwargs = self.loaders[file_type][1],
            show_progress=True,
            silent_errors=True 
        )
    
    def load_data(self):
        html_loader = self.create_directory_loader('.html',self.data_directory)
        for batch in self.batch_generator(html_loader.lazy_load(), batch_size= self.batch_size):
            self.process_batch(batch)
    

    def process_batch(self,batch):
        
        text_splitter = RecursiveCharacterTextSplitter(
            separators= configuration.CHUNK_SEPERATORS,
            chunk_size=configuration.CHUNK_SIZE,
            chunk_overlap=configuration.CHUNK_OVERLAP
        )
        split_docs = text_splitter.split_documents(batch)
        total_docs_in_this_batch = len(split_docs)
        ids = ['doc_'+str(i+self.docs_processed_till_now) for i in range(total_docs_in_this_batch)]
        # print("split_docs = ",split_docs)
        # print("total_docs_in_this_batch = ",total_docs_in_this_batch)
        # print("ids = ",ids)
        self.vectorDatabase.add_data(documents=split_docs,ids=ids)
        self.docs_processed_till_now += total_docs_in_this_batch
        # print("docs_processed_till_now = ",self.docs_processed_till_now)
        # print("-----------------------------")
    

dataProcess = DataProcess()
# dataProcess.load_data()
print(dataProcess.vectorDatabase.get_data())


