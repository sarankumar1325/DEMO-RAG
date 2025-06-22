# 📄 Document RAG Assistant

A powerful Document-based Retrieval Augmented Generation (RAG) system built with ChromaDB, Google's Gemini 2.0 Flash, and Streamlit. Upload PDF documents and ask questions based strictly on their content - no hallucinations, only factual answers from your documents.

## 🚀 Features

- **📁 PDF Document Upload**: Extract text from PDF files automatically
- **🔍 Smart Text Chunking**: Intelligently splits documents for optimal retrieval
- **🎯 Semantic Search**: Find relevant document sections using vector similarity
- **🤖 Anti-Hallucination AI**: Responses based only on document content
- **📖 Source Attribution**: See exactly which document sections were used
- **🗑️ Database Management**: Clear and manage your document collection
- **⚡ Real-time Processing**: Fast document processing and query responses

## 🛠️ Setup

### Prerequisites
- Python 3.8+
- Gemini API key from Google AI Studio

### Installation

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd "RAG DEMO"
```

2. **Install required packages**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
CHROMA_API_KEY=your_chroma_api_key_here
CHROMA_TENANT=your_chroma_tenant_id
CHROMA_DATABASE=your_database_name
```

4. **Run the application**:
```bash
streamlit run app.py
```

## 📋 Usage Guide

### 1. Upload Documents
- Click **"Choose a PDF file"** to upload your document
- Wait for processing (text extraction + chunking)
- See confirmation with chunk count and preview

### 2. Ask Questions
- Type your question in the text input field
- Click **"🔍 Get Answer"** to search and generate response
- Review the AI answer and source document sections

### 3. Manage Documents
- Use the sidebar to see document chunk count
- Click **"🗑️ Clear Database"** to remove all documents
- Upload multiple documents for cross-document queries

## 🎯 Key Benefits

### ✅ **No Hallucinations**
- AI responds only based on uploaded document content
- Says "I don't know" when information isn't available
- No external knowledge or made-up information

### ✅ **Source Transparency**
- Shows relevant document sections used for answers
- Displays filename and chunk information
- Enables fact-checking and verification

### ✅ **Smart Retrieval**
- Uses semantic similarity for relevant content discovery
- Configurable chunk size (1000 chars) with overlap (200 chars)
- Retrieves top 5 most relevant sections per query

## 🏗️ Architecture

```
PDF Upload → Text Extraction → Text Chunking → Vector Embeddings → ChromaDB Storage
                                                                            ↓
User Query → Semantic Search → Relevant Chunks → Context Building → Gemini 2.0 → Response
```

## 🔧 Technical Components

- **[Streamlit](https://streamlit.io/)**: Web interface and user experience
- **[ChromaDB](https://www.trychroma.com/)**: Vector database for document storage
- **[Google Gemini 2.0 Flash](https://ai.google.dev/)**: Large language model for response generation
- **[PyPDF2](https://pypdf2.readthedocs.io/)**: PDF text extraction
- **[LangChain](https://langchain.com/)**: Text splitting and chunking utilities

## 📁 Project Structure

```
RAG DEMO/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (not in git)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## ⚙️ Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google AI Studio API key
- `CHROMA_API_KEY`: ChromaDB cloud API key (optional)
- `CHROMA_TENANT`: ChromaDB tenant ID (optional)
- `CHROMA_DATABASE`: ChromaDB database name (optional)

### Chunking Parameters
- **Chunk Size**: 1000 characters (adjustable in code)
- **Chunk Overlap**: 200 characters (prevents information loss)
- **Retrieval Count**: 5 most relevant chunks per query

## 🔒 Security

- API keys stored in environment variables
- `.env` file excluded from version control
- No sensitive data in code repository
- Local ChromaDB instance for privacy

## 🚫 Limitations

- **PDF Only**: Currently supports PDF documents only
- **Text-based**: Cannot process images, tables, or complex layouts
- **Memory Storage**: Uses in-memory ChromaDB (data lost on restart)
- **Single Session**: No persistent user sessions or multi-user support

## 🛣️ Future Enhancements

- [ ] Support for Word documents, text files, and web pages
- [ ] Persistent ChromaDB storage
- [ ] Multi-user authentication and sessions
- [ ] Advanced document preprocessing (tables, images)
- [ ] Conversation history and follow-up questions
- [ ] Document comparison and analysis features

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

If you encounter any issues or have questions:
- Check the troubleshooting section in the app
- Review error messages in the Streamlit interface
- Ensure your API keys are correctly configured
- Verify PDF files contain extractable text

---

**Happy Document Querying! 🎉**
