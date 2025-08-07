def list_shoes_products() -> str:
    """List all available shoes products."""

    output_template = """
    Here is the desired output structure:
        👟 Model: 
        🏷️ Brand: 
        🏢 Manufacturer: 
        📁 Category: 
        🧑 Department: 
        💸 Price: 
        📏 Shoe Width: 
        🧵 Outer Material: 
        🦶 Sole: 
        🔒 Closure: 
        📐 Dimensions: 
        ⚖️ Weight: 
    """
    return output_template.strip()