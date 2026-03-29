# 📚 LearnMate – AI-Powered Learning Assistant

> Learn from videos and PDFs, ask questions with sources, and test yourself with adaptive quizzes.

LearnMate is an AI-based learning system that integrates content from multiple YouTube videos and PDF documents into a single interactive platform. Using Retrieval-Augmented Generation (RAG), it enables users to ask questions, receive accurate answers with source references, and generate adaptive quizzes for effective self-assessment.

---

## 🚀 Features

### 📺 Multi-Source Learning

* Add multiple YouTube video links
* Upload multiple PDF documents
* Automatically extracts and processes content

### ❓ Question Answering (RAG)

* Ask questions from uploaded content
* Get accurate, context-aware answers
* Includes source references:

  * 📍 YouTube timestamps
  * 📄 PDF page numbers

### 🧠 Adaptive Quiz Generation

* Generate quizzes based on:

  * Number of questions
  * Difficulty level
  * Topics
  * Selected sources (optional)
* Instant scoring with percentage-based evaluation

---

## ⚙️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **LLM:** Gemini (for answer generation and quiz creation)
* **Vector Database:** FAISS
* **Embeddings:** all-MiniLM-L6-v2
* **Data Processing:**

  * YouTube Transcript API
  * PyMuPDF (fitz) for PDF text extraction

---

## ▶️ How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/learnmate.git
cd learnmate
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
cd backend/app streamlit run  main.py
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory and add the following:

```env
# Gemini API Key
GOOGLE_API_KEY=your_api_key_here

# Model configuration
GEMINI_MODEL=gemini-2.5-flash

# Retrieval settings
MAX_CONTEXT_LENGTH=2000
TOP_K=3

# App settings
ENV=development
DEBUG=True
```


---

## 💡 Use Cases

* Learn from multiple videos in one place
* Ask doubts and get answers with references
* Revise concepts using generated quizzes
* Combine learning from PDFs and videos

---

## 📊 Example Outputs

### ✅ Answer with Source

```
Answer: Gradient descent is an optimization algorithm used to minimize loss...
Source: YouTube (02:30)
```

### 📝 Quiz Example

```
Q1. What is overfitting?
A. ...
B. ...
C. ...
D. ...

Score: 80%
```

---

## 🚧 Future Improvements

* Improved retrieval (hybrid search)
* UI enhancements
* Personalized quiz generation
* Support for additional file formats

---

## 👨‍💻 Authors

* [Karan Tekchandani](https://github.com/Karan3705)
* [Ayush Singhal](https://github.com/ayush-3107)
