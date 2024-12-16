from langsmith import Client
from datetime import datetime, timedelta
import src.ai_arnfi.config.configuration as configuration
import pandas as pd

def upload_dataset_to_langsmith(evaluation_dataframe):
    
    client = Client(timeout_ms=3600000)
    
    dataset = []
    for index, row in evaluation_dataframe.iterrows():
        dataset.append((row["query"], row["reference_answer"]))
        
    refined_dataset = list(set(dataset))
    print(refined_dataset)
    
    langsmith_dataset = client.create_dataset(
        dataset_name="Sample Evaluation Test - AARNFI ET003(SmallDataset_size_5)",
        description="Sample Evaluation Dataset of just query and answer(SmallDataset of size 5)"
    )
    
    count = 0
    for query, relevant_answer in refined_dataset:
        client.create_example(
            inputs={"question": query},
            outputs={"answer":relevant_answer},
            metadata={"source":"llm generaterd answers using llamaindex"},
            dataset_id=langsmith_dataset.id
        )
        count += 1
        if count == 5:
            break
        
        
 
evaluation_dataframe = pd.read_csv(configuration.EVALUATION_DATA_FILE_PATH)
upload_dataset_to_langsmith(evaluation_dataframe)