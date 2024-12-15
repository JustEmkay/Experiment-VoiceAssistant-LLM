# RAG (Retrieval-Augmented Generation) Pipeline

A Python-based implementation of a Retrieval-Augmented Generation (RAG) pipeline that integrates **ChromaDB**, **spaCy**, and **Ollama** for building context-aware AI solutions. This project combines document storage and retrieval with sentiment analysis and text generation.

---

## Features

1. **Vector Database Management**:
   - Store, query, and retrieve text data using **ChromaDB**.
   - Prevent duplicate entries with similarity-based checks.

2. **Sentiment Analysis**:
   - Perform sentiment and subjectivity analysis using **spaCy** and the `spacytextblob` library.
   - Extract entities from text.

3. **AI-Powered Responses**:
   - Use the **Ollama LLM** for generating concise and context-aware responses.
   - Integrate retrieved data for enhanced text generation.

4. **Retrieval-Augmented Generation**:
   - Augment user queries with relevant retrieved context.
   - Generate responses using a combination of retrieved data and AI capabilities.

---

## Installation

Follow the steps below to set up the project:

### Prerequisites

- Python 3.9 or later installed.
- Basic familiarity with virtual environments is recommended.

### 1. Install Dependencies

Install the required packages from requirements.txt:
```
pip install -r requirements.txt
```
### 2. Additional Configuration

For Vector Database:
*   ChromaDB will create and manage the database in the current directory.

For Sentiment Analysis:
*   Download the en_core_web_sm model for spaCy:

```
python -m spacy download en_core_web_sm
```

For Ollama LLM:
*   Ensure the Ollama CLI is installed and running on your system.
*   Install models for Ollama using:
```
ollama pull <model_name> #Example: ollama pull llama3.2:1b
```
Or 
```
ollama run <model_name> #Example: ollama run llama3.2:1b
```

---

## Usage

### 1. Initialize the Components
Use the RAG class to start the pipeline:

```
from your_module import RAG

rag = RAG(model_name="your-ollama-model")
```

### 2. Insert Data into the VectorDB
Add text data into the vector database for retrieval:
```
data = [
    {"id": "1", "text": "This is a test document."},
    {"id": "2", "text": "Another example document."}
]
response = rag.vectorDB.insertToDB(data)
print(response)
```

### 3. Query and Generate Responses
Retrieve relevant context and generate AI responses:
```
query = "Tell me about the test document."
response = rag.generate(query)
print(response)
```

### 4. Perform Sentiment Analysis
Analyze the sentiment of a specific text:

```
text = "I love this project!"
result = rag.sentiment_analysis(text)
print(result)
```

---

## Key Components
### 1. VectorDB
Handles storage, retrieval, and duplicate detection for text data using ChromaDB.

### 2. OllamaLLM
Facilitates interaction with Ollama models for chat-based text generation.

### 3. RAG
The main pipeline that combines vector retrieval, sentiment analysis, and language model generation

---

<!-- ## License

SpotDash is open-source and under the [MIT License](LICENSE.md). -->