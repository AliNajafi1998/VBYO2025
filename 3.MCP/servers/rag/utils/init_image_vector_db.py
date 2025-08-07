import chromadb
import json

output_dir = "/Users/alinajafi/Documents/AmazonAssistant/servers/rag/data/shoesDB"
chroma_client = chromadb.PersistentClient(path=output_dir)
 
# Creating collection
img_collection = chroma_client.create_collection(
    name="shoe_img_database",
    metadata={"hnsw:space": "cosine"} # The similarity measure used to get query neighbours
    ) # You can define an embedding function here


# Loading product data (Show dataset and data preparation)
path = f"/Users/alinajafi/Documents/AmazonAssistant/servers/rag/data/amazon_shoe_database.jsonl"
with open(path, "r") as f:
    data = []
    for line in f:
        doc = json.loads(line)
        data.append(doc)


img_embeddings = {}
path = f"/Users/alinajafi/Documents/AmazonAssistant/servers/rag/data/jinaai_image_embeddings.jsonl"
with open(path, "r") as f:
    for line in f:
        embedding_info = json.loads(line)
        item_id = embedding_info["product_id"]
        embedding = embedding_info["embedding"]
        img_embeddings[item_id] = embedding


document_ids = [product_id for product_id in img_embeddings.keys()]
docs_by_id = {doc["id"]: doc for doc in data}
documents = [docs_by_id[doc_id]["text"] for doc_id in document_ids]
metadatas = []

for doc_id in document_ids:
  doc = docs_by_id[doc_id]
  metadata = {key: doc[key] for key in ["url", "closure", "price", "brand", "department"]}
  metadatas.append(metadata)

embeddings = [img_embeddings[doc_id] for doc_id in document_ids]

# Batch Insertion, you cannot index all the data at once
max_batch_size = chroma_client.get_max_batch_size()
for batch_index in range(0, len(embeddings), max_batch_size):
    img_collection.add(
        embeddings=embeddings[batch_index:batch_index + max_batch_size],
        documents=documents[batch_index:batch_index + max_batch_size],
        metadatas=metadatas[batch_index:batch_index + max_batch_size],
        ids=document_ids[batch_index:batch_index + max_batch_size]
    )