from transformers import AutoModel
import chromadb
import os



embedding_model = AutoModel.from_pretrained("jinaai/jina-clip-v1", trust_remote_code=True)

# A dictionary that maps each product ID to its image path
images_dir = f"/Users/alinajafi/Documents/AmazonAssistant/servers/rag/data/images/images"
id2image = {
    file_name.split(".")[0]: os.path.join(images_dir, file_name) for file_name in os.listdir(images_dir)
}


def search_amazon_shoes_by_text(query: str, n:int=5) -> str:
    db_dir = "/Users/alinajafi/Documents/AmazonAssistant/servers/rag/data/shoesDB"
    chroma_client = chromadb.PersistentClient(path=db_dir)

    collection = chroma_client.get_collection("shoes_doc_collection")


    query_embedding = embedding_model.encode_text(query, show_progress_bar=False) 
    relevant_data = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n, 
    )
    docs = relevant_data["documents"][0]

    return docs


def search_amazon_shoes_with_images(query: str, n:int=5) -> str:
    db_dir = "/Users/alinajafi/Documents/AmazonAssistant/servers/rag/data/shoesDB"
    chroma_client = chromadb.PersistentClient(path=db_dir)

    collection = chroma_client.get_collection("shoe_img_database")

    query_embedding = embedding_model.encode_text(query, show_progress_bar=False) 
    relevant_data = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n, 
    )
    # docs = relevant_data["documents"][0]

    product_ids = relevant_data["ids"][0]

    image_paths = [id2image[product_id] for product_id in product_ids]

    return image_paths