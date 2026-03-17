import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ingestion
from ingestion.youtube_loader import load_youtube_transcript

# processing
from processing.transcript_cleaner import clean_documents
from processing.chunking import chunk_documents

# embeddings
from embeddings.embedding_model import EmbeddingModel

# rag pipeline
from rag.qa_pipeline import qa_pipeline

# ✅ NEW: citation handler
from rag.citation_handler import format_citations, print_citations


def main():

    # -------------------------
    # Step 1: Load YouTube Video
    # -------------------------

    youtube_url = "https://www.youtube.com/watch?v=aircAruvnKk"

    print("\n📥 Loading YouTube captions...")

    raw_docs = load_youtube_transcript(youtube_url)

    if not raw_docs:
        print("❌ No transcript data found.")
        return

    # -------------------------
    # Step 2: Normalize Documents
    # -------------------------

    documents = []

    for d in raw_docs:
        documents.append({
            "text": d["text"],
            "metadata": {
                "source": "youtube",
                "video_url": youtube_url,
                "title": "Neural Networks Explained",  # you can later auto-fetch
                "timestamp": d["timestamp"],
                "start_seconds": d["timestamp_seconds"],
                "end_seconds": d["chunk_end_seconds"],
                "link": d["source"]
            }
        })

    print(f"✅ Loaded {len(documents)} transcript chunks")

    # -------------------------
    # Step 3: Clean Documents
    # -------------------------

    print("\n🧹 Cleaning documents...")

    clean_docs = clean_documents(documents)

    # -------------------------
    # Step 4: Chunk Documents
    # -------------------------

    print("\n✂️ Chunking documents...")

    chunks = chunk_documents(clean_docs)

    print(f"✅ Total chunks: {len(chunks)}")

    # -------------------------
    # Step 5: Generate Embeddings
    # -------------------------

    print("\n🧠 Generating embeddings...")

    embedding_model = EmbeddingModel()

    embedded_docs = embedding_model.embed_documents(chunks)

    print(f"✅ Embeddings created for {len(embedded_docs)} chunks")

    # -------------------------
    # Step 6: Ask Question
    # -------------------------

    query = "What is a neural network?"

    print("\n💬 Running QA pipeline...")

    answer, sources = qa_pipeline(query, embedded_docs)

    # -------------------------
    # Step 7: Format Citations
    # -------------------------

    citations = format_citations(sources)

    # -------------------------
    # Step 8: Print Result
    # -------------------------

    print("\n📌 QUESTION:\n", query)

    print("\n📢 ANSWER:\n", answer.strip())

    print_citations(citations)


if __name__ == "__main__":
    main()