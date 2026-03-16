import faiss
import numpy as np


def create_faiss_index(embedded_docs):
    """
    embedded_docs = [
        {
            "text": "...",
            "embedding": [...],
            "source": "...",
            "timestamp/page": "..."
        }
    ]
    """

    # extract embeddings
    embeddings = [doc["embedding"] for doc in embedded_docs]

    # convert to numpy
    vectors = np.array(embeddings).astype("float32")

    # embedding dimension
    dimension = vectors.shape[1]

    # create FAISS index
    index = faiss.IndexFlatL2(dimension)

    # add vectors
    index.add(vectors)

    return index