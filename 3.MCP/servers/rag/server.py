import json
import os

from tools import search_amazon_shoes_by_text, search_amazon_shoes_with_images
from prompts import list_shoes_products
from resources import load_shoes_memories, list_shoes_memories_file_names

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv("../.env")

mcp = FastMCP(
    name="Amazon Assistant",
    host="0.0.0.0",
    port=8000,
)

@mcp.tool(name="search_amazon_shoes")
def search_amazon_shoes(query: str, n: int=5) -> str:
    """
    Search for shoes on Amazon. 
    Args:
        query (str): The search query for shoes.
        n (int): The number of results to return. Default is 5.
    Returns:
        str: A JSON string containing the search results.
    """

    results = search_amazon_shoes_by_text(query, n=n)
    return json.dumps({"result": results})


@mcp.tool(name="search_amazon_shoes_with_images")
def search_amazon_shoes_having_images(query: str, n: int=5) -> str:
    """
    Search for shoes on Amazon with images.
    Args:
        query (str): The search query for shoes.
        n (int): The number of results to return. Default is 5.
    Returns:
        str: A JSON string containing the search results with images.
    """
    results = search_amazon_shoes_with_images(query, n=n)

    return json.dumps({"Images": results})


@mcp.prompt()
async def list_shoes_products_prompt() -> str:
    """"
    This prompt gives the structure for listing shoes products.
    It is used to format the output of the shoes products.
    Returns:
        str: A formatted string that describes the structure of shoes products.
    """
    return list_shoes_products()


@mcp.tool(name="save_shoes")
async def save_shoes_memory(shoe_type: str, data: dict) -> str:
    """
    Save shoes memory to a dynamic schema.
    Args:
        shoe_type (str): The type of shoes to save.
        data (dict): The data to save.
    Returns:
        str: A confirmation message.
    """
    with open(f"/Users/alinajafi/Documents/AmazonAssistant/servers/rag/data/memory/{shoe_type}.json", "w") as f:
        json.dump(data, f)
    return f"Memory for {shoe_type} saved successfully."


# @mcp.resource("shoes://load/{shoe_type}")
# async def get_shoes_memory(shoe_type: str) -> dict:
#     """ Load shoes memories from a file."""
#     return load_shoes_memories(shoe_type)


@mcp.tool(name="load_shoes_memory_by_type")
async def get_shoes_memory(shoe_type: str) -> dict:
    """ Load shoes memories from a file."""
    return load_shoes_memories(shoe_type)


@mcp.resource("shoes://list")
async def list_shoes_memory() -> dict:
    """ List all shoes memories log file names."""
    return list_shoes_memories_file_names()

if __name__ == "__main__":
    transport = "stdio"  # Change to "sse" for SSE transport
    if transport == "sse":
        print("Running with SSE transport")
        mcp.run(transport="sse")
    elif transport == "stdio":
        print("Running with STDIO transport")
        mcp.run(transport="stdio")
    else:
        raise ValueError("Unsupported transport type. Use 'sse' or 'stdio'.")
