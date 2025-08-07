import chromadb
import json


# Initializing client
output_dir = "/Users/alinajafi/Documents/AmazonAssistant/servers/rag/data/shoesDB"
chroma_client = chromadb.PersistentClient(path=output_dir)
# Creating collection
doc_collection = chroma_client.create_collection(
    name="shoes_doc_collection",
    metadata={"hnsw:space": "cosine"} # The similarity measure used to get query neighbours
    ) # You can define an embedding function here


# Loading product data (Show dataset and data preparation)
path = f"/Users/alinajafi/Documents/AmazonAssistant/servers/rag/data/amazon_shoe_database.jsonl"
with open(path, "r") as f:
    data = []
    for line in f:
        doc = json.loads(line)
        data.append(doc)

 

# Loading document embeddings
doc_embeddings = {}
path = f"/Users/alinajafi/Documents/AmazonAssistant/servers/rag/data/jinaai_doc_embeddings.jsonl"
with open(path, "r") as f:
    for line in f:
        embedding_info = json.loads(line)
        item_id = embedding_info["product_id"]
        embedding = embedding_info["embedding"]
        doc_embeddings[item_id] = embedding




document_ids = [doc["id"] for doc in data]
documents = [doc["text"] for doc in data]
metadatas = []

for doc in data:
  metadata = {key: doc[key] for key in ["url", "closure", "price", "brand", "department"]}
  metadatas.append(metadata)

embeddings = [doc_embeddings[doc_id] for doc_id in document_ids]

# Batch Insertion, you cannot index all the data at once
max_batch_size = chroma_client.get_max_batch_size()
for batch_index in range(0, len(embeddings), max_batch_size):
    doc_collection.add(
        embeddings=embeddings[batch_index:batch_index + max_batch_size],
        documents=documents[batch_index:batch_index + max_batch_size],
        metadatas=metadatas[batch_index:batch_index + max_batch_size],
        ids=document_ids[batch_index:batch_index + max_batch_size]
    )

# # Save the collection to disk

# chroma_client.persist(output_dir=output_dir)
# print("Collection created and data indexed successfully.")