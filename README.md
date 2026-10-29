# 🚀 Doc Intel RAG API

An AI-powered document intelligence application built using **FastAPI, LangChain, Google Gemini, and ChromaDB**.

Doc Intel RAG API allows users to upload multiple documents, convert their content into embeddings, store them in a vector database, and ask questions using Retrieval-Augmented Generation (RAG). The application retrieves relevant document content and uses Google Gemini to generate context-aware answers with source citations.

## ✨ Features

- FastAPI REST API integration
- Google Gemini LLM integration
- Google Gemini embeddings
- ChromaDB vector storage
- SQLite metadata storage
- PDF, DOCX, and TXT document support
- Single and multiple file uploads
- Duplicate file detection using SHA-256
- Semantic search and similarity retrieval
- Retrieval-Augmented Generation (RAG)
- Conversation history using session IDs
- Source citations for answers
- Document listing and deletion
- Debug endpoints for retrieval and vector storage
- Modular backend architecture

## 🏗️ Architecture

```text
                 User Question
                       |
                       v
                 FastAPI REST API
                       |
                       v
                 Retrieval Service
                       |
                       v
                ChromaDB Vector Store
                       |
                       v
                Relevant Document Chunks
                       |
                       v
                  Google Gemini
                       |
                       v
              Context-Aware AI Answer
              with Source Citations
```

## 📁 Project Structure

```text
doc-intel-rag-api/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── uploaded_docs/
├── chroma_db/
├── app_data/
│
├── requirements.txt
├── .env
└── README.md
```

*Note: The directory structure above represents the intended organization. Adjust it to match the actual files in your repository.*

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| LangChain | LLM integration and RAG orchestration |
| Google Gemini | AI response generation |
| Gemini Embeddings | Text vectorization |
| ChromaDB | Vector database and similarity search |
| SQLite | Metadata and application data storage |
| Uvicorn | ASGI server |

## 📦 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/suhas2357/doc-intel-rag-api.git
cd doc-intel-rag-api
```

### 2. Create a Virtual Environment

**Windows — PowerShell**

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

If you use Command Prompt:

```bat
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and configure the required settings.

```env
GOOGLE_API_KEY=your_google_api_key

LLM_MODEL=gemini-1.5-flash
EMBEDDING_MODEL=models/gemini-embedding-2

UPLOAD_DIR=uploaded_docs
CHROMA_PERSIST_DIR=chroma_db
SQLITE_DB_PATH=app_data/rag.db

COLLECTION_NAME=rag_documents

CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=4

MAX_FILE_SIZE_MB=10
MAX_FILES_PER_UPLOAD=10

SUPPORTED_EXTENSIONS=.pdf,.txt,.docx

MAX_HISTORY_MESSAGES=10
```

**Important:** These environment variable names and model identifiers must match those supported by your implementation and the Google AI API. Replace the placeholder API key with your own key, and never commit real API credentials to GitHub.

## ▶️ Run the Application

From the project root, run:

```bash
uvicorn app.main:app --reload
```

Once the server starts, open the following URLs:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

Use Swagger UI to explore and test the available API endpoints.

## 📄 Supported Document Formats

| Format | Extension |
|---|---|
| PDF | `.pdf` |
| Microsoft Word | `.docx` |
| Plain text | `.txt` |

## 🔄 How RAG Works

1. **Document Upload:** The user uploads one or more documents.
2. **Document Loading:** The application extracts text from the uploaded files.
3. **Text Chunking:** The extracted text is divided into smaller chunks.
4. **Embedding Generation:** Gemini embeddings convert the text chunks into vector representations.
5. **Vector Storage:** Chunks and associated metadata are stored in ChromaDB.
6. **Question Processing:** The user submits a question through the API.
7. **Semantic Retrieval:** The application retrieves relevant document chunks.
8. **Context Injection:** Retrieved content is provided to the language model.
9. **Answer Generation:** Gemini generates a response grounded in the retrieved context.
10. **Source Citation:** The response can include references to relevant source documents.

## 🔌 API Endpoints

The following endpoints describe the documented application interface. Confirm their exact paths and request schemas in Swagger UI.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/rag/upload` | Upload a single document |
| `POST` | `/rag/upload-multiple` | Upload multiple documents |
| `POST` | `/rag/ask` | Ask a question about uploaded documents |
| `GET` | `/rag/documents` | List uploaded documents |
| `DELETE` | `/rag/documents/{document_id}` | Delete a document |
| `GET` | `/rag/chat-history/{session_id}` | Retrieve conversation history |
| `DELETE` | `/rag/chat-history/{session_id}` | Clear conversation history |
| `GET` | `/rag/debug/vector-store` | Inspect vector store information |
| `POST` | `/rag/debug/retrieve` | Test document retrieval |

### Example: Ask a Question

**Request**

```http
POST /rag/ask
Content-Type: application/json
```

**Example JSON body**

```json
{
  "question": "What is maternity leave?",
  "session_id": "employee001"
}
```

The application uses the question and relevant retrieved document content to generate an answer. The exact response format depends on the API schema.

## 🧠 Key Concepts

- Retrieval-Augmented Generation (RAG)
- Text embeddings and vector representations
- Semantic search
- Document chunking and overlap
- Vector databases
- Similarity-based retrieval
- Metadata management
- Prompt engineering
- Context injection
- Conversation history
- FastAPI routing and dependency injection
- Modular backend development
- API validation and error handling

## 🚀 Future Improvements

- CSV, Excel, Markdown, HTML, and PowerPoint support
- OCR for scanned documents
- Image-based question answering
- Hybrid search using BM25 and vector retrieval
- Cross-encoder reranking
- Streaming AI responses
- User authentication and authorization
- Docker containerization
- Cloud deployment
- CI/CD automation
- Automated testing and monitoring

## 👨‍💻 Author

**Suhas Sonwane**

Python Backend Developer | AI Application Development

**Technologies:** Python, FastAPI, LangChain, RAG, Google Gemini, ChromaDB, SQLite

- GitHub: https://github.com/suhas2357
- Project Repository: https://github.com/suhas2357/doc-intel-rag-api

## ⭐ Support

If you find this project useful, consider giving the repository a star on GitHub!
