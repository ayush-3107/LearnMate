from sentence_transformers import SentenceTransformer
import numpy as np

# load same embedding model used earlier
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_documents(query, index, embedded_docs, k=3):
    """
    query : user question
    index : FAISS index
    embedded_docs : original documents with embeddings
    k : number of results
    """

    # convert query to embedding
    query_embedding = model.encode([query])

    query_vector = np.array(query_embedding).astype("float32")

    # search in FAISS
    distances, indices = index.search(query_vector, k)

    # retrieve original documents
    results = [embedded_docs[i] for i in indices[0]]

    return results