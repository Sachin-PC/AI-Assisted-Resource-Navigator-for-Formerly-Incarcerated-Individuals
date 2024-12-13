import json
import src.ai_arnfi.config.configuration as configuration
import numpy as np

def store_evaluation_data_to_json(evaluation_data):
    evaluation_data_file = configuration.EVALUATION_DATA_FILE_PATH
    
    with open(evaluation_data_file, "w") as json_file:
        json.dump(evaluation_data, evaluation_data_file, indent=4)
        
    print(f"Data Successfully saved to {evaluation_data_file}.")