from llama_index.core.llama_pack import download_llama_pack
import pandas as pd
import src.ai_arnfi.config.configuration as configuration

class ResponseEvaluator:
    def __init__(self):
       self.RagEvaluatorPack = download_llama_pack("RagEvaluatorPack", "./pack")
       self.rag_dataset = pd.read_csv(configuration.EVALUATION_DATA_FILE_PATH)

def evaluate_response():
    return