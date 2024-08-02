import os
import logging
import json
import pandas as pd

def setup_logging(log_file='app.log'):
    """
    Setup logging configuration.
    
    Args:
        log_file (str): Path to the log file.
    """
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(message)s')
    logging.info("Logging setup complete.")

def save_json(data, file_path):
    """
    Save Data to a JSON file.
    
    Args:
        data (dict): Data to be saved.
        file_path (str): Path to the JSON file.
    """
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    logging.info(f"Data saved to {file_path}")

def load_json(file_path):
    """
    Load Data from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file.
    
    Returns:
        dict: Loaded Data.
    """
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    logging.info(f"Data loaded from {file_path}")
    return data

def save_to_csv(data, file_path):
    """
    Save Data to a CSV file.
    
    Args:
        data (pd.DataFrame): Data to be saved.
        file_path (str): Path to the CSV file.
    """
    data.to_csv(file_path, index=False)
    logging.info(f"Data saved to {file_path}")

def load_from_csv(file_path):
    """
    Load Data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Loaded Data.
    """
    data = pd.read_csv(file_path)
    logging.info(f"Data loaded from {file_path}")
    return data

# Example usage
if __name__ == "__main__":
    setup_logging()

    # Example: Save and load JSON
    data = {'name': 'John Doe', 'age': 30}
    save_json(data, 'Data.json')
    loaded_data = load_json('Data.json')
    print(loaded_data)

    # Example: Save and load CSV
    df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [25, 30]})
    save_to_csv(df, 'Data.csv')
    loaded_df = load_from_csv('Data.csv')
    print(loaded_df)
