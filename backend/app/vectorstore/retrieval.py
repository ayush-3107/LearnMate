from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_documents(query, index, embedded_docs, k=3):
    """
    Retrieve top-k similar documents using FAISS
    """

    # -------------------------
    # Step 1: Encode query
    # -------------------------
    query_embedding = model.encode([query])
    query_vector = np.array(query_embedding).astype("float32")

    # Normalize (important for cosine similarity behavior)
    faiss.normalize_L2(query_vector)

    # -------------------------
    # Step 2: Search
    # -------------------------
    distances, indices = index.search(query_vector, k)

    # -------------------------
    # Step 3: Safe retrieval
    # -------------------------
    results = []
    for i in indices[0]:
        if i != -1 and i < len(embedded_docs):
            results.append(embedded_docs[i])

    return results