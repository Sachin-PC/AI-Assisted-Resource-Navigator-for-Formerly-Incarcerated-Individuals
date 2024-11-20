EMBEDDING_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1" # check out model details here: https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1

#Chunking Parameters
CHUNK_SEPERATORS = ["\n\n", "\n", " ", ""]
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100


#MODEL PARAMETERS
MODEL_NAME = "gpt-3.5-turbo"
MODEL_TEMPERATURE = 0
MODEL_WAIT_FOR_MODEL = True
MODEL_PARAMETERS = {
    "wait_for_model": True,
    "do_sample": False,
    "temperature": 0.7,
    "top_p": 0.9,
    "return_full_text": False,
    "max_new_tokens": 1024
}
MODEL_TASK = "text-generation"

#DATA PARAMETERS
DATA_DIRECTORY = "/Users/sachinpc/Documents/GitHubProjects/AI_FOR_HCI/TempData/data_files/"

#Vector database
VECTOR_DB_DIRECTORY = "/Users/sachinpc/Documents/GitHubProjects/AI_FOR_HCI/AI-Assisted-Resource-Navigator-for-Formerly-Incarcerated-Individuals/database/vector_database/chroma_db"
VECTOR_DB_COLLECTION_NAME = 'legal_data_documents'