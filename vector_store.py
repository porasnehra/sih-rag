import os
import json
import faiss
import numpy as np
from google import genai
from dotenv import load_dotenv
from models import SessionLocal, StandardRecord

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

EMBEDDING_MODEL = "gemini-embedding-2"
INDEX_FILE = "faiss_index.bin"
METADATA_FILE = "faiss_metadata.json"

def get_embedding(text):
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )
    return result.embeddings[0].values

def get_query_embedding(text):
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )
    return result.embeddings[0].values

def build_vector_store():
    session = SessionLocal()
    records = session.query(StandardRecord).all()
    session.close()

    embeddings = []
    metadata = []

    print(f"Embedding {len(records)} records...")
    for idx, record in enumerate(records):
        # Create a semantic chunk representing the record
        text_chunk = f"Standard Number: {record.is_number}\nTitle: {record.title}\nScope: {record.scope}\nProduct Category: {record.product_category}\nCertification: {record.certification_scheme}\nTesting Requirements: {record.testing_requirements}\nLabs: {record.lab_info}"
        
        emb = get_embedding(text_chunk)
        embeddings.append(emb)
        metadata.append(record.to_dict())
        
        if (idx + 1) % 5 == 0:
            print(f"Processed {idx + 1} records.")

    embeddings_np = np.array(embeddings).astype('float32')
    
    # FAISS setup
    dim = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings_np)
    
    # Save index and metadata
    faiss.write_index(index, INDEX_FILE)
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=2)
        
    print(f"Saved FAISS index with {index.ntotal} vectors of dimension {dim}.")

def load_vector_store():
    index = faiss.read_index(INDEX_FILE)
    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)
    return index, metadata

def search_vectors(query, k=3, product_category=None):
    index, metadata = load_vector_store()
    query_emb = np.array([get_query_embedding(query)]).astype('float32')
    
    distances, indices = index.search(query_emb, k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        meta = metadata[idx]
        
        # Simple post-filtering for demo purposes
        if product_category and product_category.lower() not in meta['product_category'].lower():
            continue
            
        results.append({
            "score": float(distances[0][i]),
            "metadata": meta
        })
        
    return results

if __name__ == "__main__":
    build_vector_store()
