from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Minimum similarity score to consider a chunk relevant
# Range: 0.0 (anything) to 1.0 (exact match). 0.4 is a good balance.
SIMILARITY_THRESHOLD = float(0.4)

def retrieve_documents(query, index, embedded_docs, k=3):
    """
    Retrieve top-k similar documents using FAISS.
    Only returns chunks above SIMILARITY_THRESHOLD — if none pass,
    returns empty list so the LLM won't hallucinate from weak context.
    """
    # -------------------------
    # Step 1: Encode query
    # -------------------------
    query_embedding = model.encode([query])
    query_vector = np.array(query_embedding).astype("float32")

    # Normalize (required for cosine similarity with IndexFlatIP)
    faiss.normalize_L2(query_vector)

    # -------------------------
    # Step 2: Search
    # -------------------------
    distances, indices = index.search(query_vector, k)

    # -------------------------
    # Step 3: Filter by similarity threshold
    # distances here are cosine similarity scores (0.0 - 1.0)
    # higher = more similar
    # -------------------------
    results = []
    for score, i in zip(distances[0], indices[0]):
        if i == -1 or i >= len(embedded_docs):
            continue
        if score >= SIMILARITY_THRESHOLD:
            results.append(embedded_docs[i])

    return results