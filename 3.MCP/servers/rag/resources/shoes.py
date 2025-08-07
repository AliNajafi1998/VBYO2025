import os
import json

def load_shoes_memories(shoe_type: str) -> dict:
    """
    Load shoes memories from a dynamic schema.
    Args:
        shoe_type (str): The type of shoes to load.
    Returns:
        dict: A dictionary containing the loaded data.
    """
    file_path = f"/Users/alinajafi/Documents/AmazonAssistant/servers/rag/data/memory/{shoe_type}.json"
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r") as f:
        data = json.load(f)
    
    return data

def list_shoes_memories_file_names() -> list:
    """
    List all shoes memories log file names.
    Returns:
        list: A list of file names containing shoes memories.
    """
    memory_dir = "/Users/alinajafi/Documents/AmazonAssistant/servers/rag/data/memory"
    return [file_name for file_name in os.listdir(memory_dir) if file_name.endswith(".json")]