try:
    # Newer LangChain versions expose splitters in a dedicated package.
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    # Fallback for older versions that still use langchain.text_splitter.
    from langchain.text_splitter import RecursiveCharacterTextSplitter


class TextChunker:
    """
    Splits large documents into smaller chunks
    for better embeddings and retrieval.
    """

    def __init__(self, chunk_size=500, chunk_overlap=100):
        """
        chunk_size: maximum characters per chunk
        chunk_overlap: overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def split_text(self, text: str):
        """
        Split raw text into chunks
        """
        chunks = self.splitter.split_text(text)
        return chunks

    def split_documents(self, documents):
        """
        Split list of LangChain documents
        """
        return self.splitter.split_documents(documents)


if __name__ == "__main__":

    sample_text = """
        Machine learning is a branch of artificial intelligence that focuses on enabling systems to learn patterns from data.
        Instead of being explicitly programmed, machine learning algorithms improve automatically through experience.
        These algorithms build models based on sample data in order to make predictions or decisions.

        In modern technology, machine learning plays a critical role in applications such as recommendation systems,
        computer vision, speech recognition, natural language processing, and fraud detection.
        Companies like Google, Amazon, and Netflix rely heavily on machine learning models to personalize user experiences.

        Supervised learning is one of the most common types of machine learning.
        In supervised learning, the model is trained using labeled datasets.
        Each example in the dataset contains both the input features and the correct output.
        The algorithm learns the relationship between the input and the output.

        Examples of supervised learning tasks include classification and regression.
        In classification, the goal is to predict a category or label.
        In regression, the goal is to predict a continuous numerical value.

        Unsupervised learning is another important category of machine learning.
        Unlike supervised learning, unsupervised learning does not use labeled data.
        Instead, the algorithm tries to find hidden patterns or structures within the data.

        Clustering is a common unsupervised learning technique.
        Clustering algorithms group similar data points together based on their features.
        One popular clustering algorithm is K-Means clustering.

        Dimensionality reduction is another unsupervised learning technique.
        It reduces the number of features in a dataset while preserving important information.
        Principal Component Analysis (PCA) is one widely used dimensionality reduction method.

        Reinforcement learning is a different paradigm of machine learning.
        In reinforcement learning, an agent learns by interacting with an environment.
        The agent takes actions and receives rewards or penalties based on those actions.

        The goal of reinforcement learning is to maximize the total reward over time.
        Reinforcement learning is commonly used in robotics, gaming, and autonomous systems.

        Deep learning is a subset of machine learning that uses artificial neural networks.
        These networks are inspired by the structure of the human brain.
        Deep learning models are particularly powerful for tasks involving images, audio, and text.

        Convolutional Neural Networks (CNNs) are widely used for computer vision tasks.
        Recurrent Neural Networks (RNNs) are used for sequential data such as time series and language modeling.
        Transformers have recently become the dominant architecture in natural language processing.

        Large language models like GPT are based on the transformer architecture.
        They are capable of generating human-like text and answering complex questions.
        These models are trained on massive datasets containing billions of words.

        Despite their power, machine learning models also face challenges.
        Issues such as bias, overfitting, and lack of interpretability remain important research areas.
        Researchers are constantly working to improve the reliability and fairness of machine learning systems.

        As machine learning continues to evolve, it will play an increasingly important role in science,
        healthcare, finance, transportation, and education.
        Understanding the fundamentals of machine learning is becoming an essential skill
        for engineers, data scientists, and researchers across many industries.
        """

    chunker = TextChunker()

    chunks = chunker.split_text(sample_text)

    print("Total Chunks:", len(chunks))
    for i, chunk in enumerate(chunks):
        print("\n----------------------------")
        print("Chunk", i + 1)
        print("Length:", len(chunk))
        print(chunk)