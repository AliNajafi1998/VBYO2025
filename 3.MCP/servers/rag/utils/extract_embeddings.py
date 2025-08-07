import json
import os

# If you plan to use the LangChain utilities, you can convert the JSON data to
# LangChain Documents to integrate with the LangChain library
from langchain_core.documents import Document
from tqdm import tqdm
from transformers import AutoModel

embedding_model = AutoModel.from_pretrained("jinaai/jina-clip-v1", trust_remote_code=True)
embedding_model = embedding_model.to("cuda") # Moving to GPU


data_dir = "/Users/alinajafi/Documents/AmazonAssistant/servers/rag/data"


# Loading product data (Show dataset and data preparation)
path = f"{data_dir}/amazon_shoe_database.jsonl"
with open(path) as f:
    data = []
    for line in f:
        doc = json.loads(line)
        data.append(doc)

docs = []
for item in data:
  text = item["text"]
  metadata = {key: item[key] for key in ["url", "closure", "price", "brand", "department"]}
  doc = Document.model_construct(page_content=text, id=item["id"], metadata=metadata)
  docs.append(doc)



# Creating embeddings for our documents

save_path = f"{data_dir}/jinaai_doc_embeddings.jsonl"

# Read existing doc embeddings
if os.path.exists(save_path):
  with open(save_path) as f:
    existing_docs = [json.loads(line) for line in f]
  existing_product_ids = set([doc["id"] for doc in existing_docs])
else:
  existing_product_ids = set()

doc_embeddings = []
for doc in tqdm(data):

  product_id = doc["id"]

  if product_id in existing_product_ids:
    continue

  embedding = embedding_model.encode_text(doc["text"])

  result = {
      "product_id": product_id,
      "embedding": embedding.tolist()
  }
  doc_embeddings.append(result)

  with open(save_path, "a") as f:
    f.write(json.dumps(result) + "\n")
