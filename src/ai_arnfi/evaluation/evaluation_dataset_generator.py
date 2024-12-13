from queue import PriorityQueue
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import src.ai_arnfi.config.configuration as configuration
from src.ai_arnfi.utils.common import store_evaluation_data_to_json
from llama_index.core import SimpleDirectoryReader
from llama_index.core.evaluation import DatasetGenerator
from llama_index.core.schema import Document as LlamaDocument
from llama_index.core.llama_dataset.generator import RagDatasetGenerator
from llama_index.llms.openai import OpenAI
from llama_index.core.llama_dataset import (
    LabelledRagDataExample,
)
import json
from typing import Dict, List
import pandas as pd
import time


class EvaluationDataGenerator:
    def __init__(self):
        self.loaders = {
            '.html': (UnstructuredHTMLLoader, {})
        }
        self.data_directory = configuration.DATA_DIRECTORY
        self.batch_size = 5
        self.docs_processed_till_now = 0

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
        evaluation_data = []
        evaluation_data: Dict[str, List] = {
            "query": [],
            "reference_contexts": [],
            "reference_answer": [],
            "reference_answer_by": [],
            "query_by": [],
        }
        count  = 0
        for batch in self.batch_generator(html_loader.lazy_load(), batch_size= self.batch_size):
            batch_evaluation_data = self.process_batch_rag_generator(batch)
            for example in batch_evaluation_data.examples:
                if not isinstance(example, LabelledRagDataExample):
                    raise ValueError(
                        "All examples in the dataset must be of type LabelledRagDataExample."
                    )
                evaluation_data["query"].append(example.query)
                evaluation_data["reference_contexts"].append(example.reference_contexts)
                evaluation_data["reference_answer"].append(example.reference_answer)
                evaluation_data["reference_answer_by"].append(str(example.reference_answer_by))
                evaluation_data["query_by"].append(str(example.query_by))
            count += 1
            if count == 4:
                break
            time.sleep(60)
                
        evaluation_data_dataframe = pd.DataFrame(evaluation_data)
        evaluation_data_dataframe.to_csv(configuration.EVALUATION_DATA_FILE_PATH)
    
    def convert_langchain_doc_to_llama_doc(self,langchina_document):
        return LlamaDocument(text = langchina_document.page_content,
                             extra_info = langchina_document.metadata)
    
    def process_batch_data_generator(self,batch):
        llama_documents_batch = [self.convert_langchain_doc_to_llama_doc(document) for document in batch]
        print(llama_documents_batch)
        data_generator = DatasetGenerator.from_documents(llama_documents_batch)
        eval_dataset = data_generator.generate_dataset_from_nodes(num=10)
        
    def process_batch_rag_generator(self,batch):
        llama_documents_batch = [self.convert_langchain_doc_to_llama_doc(document) for document in batch]
        print(llama_documents_batch)
        llm_model = OpenAI(model="gpt-4")
        rag_data_generator = RagDatasetGenerator.from_documents(documents=llama_documents_batch,
                                                            llm = llm_model,
                                                            num_questions_per_chunk=4)
        rag_eval_dataset = rag_data_generator.generate_dataset_from_nodes()
        return rag_eval_dataset
        

dataProcess = EvaluationDataGenerator()
dataProcess.load_data()
# dataProcess.vectorDatabase.get_data()


