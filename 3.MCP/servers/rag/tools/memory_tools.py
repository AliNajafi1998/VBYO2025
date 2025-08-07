import json

def append_shoe_memory_by_type(shoe_type: str, data: dict) -> str:
    """
    Save shoes memory to a dynamic schema.
    Args:
        shoe_type (str): The type of shoes to save.
        data (dict): The data to save.
    Returns:
        str: A JSON string containing the result of the save operation.
    """
    with open(f"memory/{shoe_type}.json", "a") as f:
        json.dump(data, f)