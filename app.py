import streamlit as st
import chromadb
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import PyPDF2
import io
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

# Configure Gemini API
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Initialize ChromaDB client (using local client for demo)
chroma_client = chromadb.Client()

# Create or get collection
collection = chroma_client.get_or_create_collection(
    name="document_chunks"
)

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=200):
    """Split text into smaller chunks for better retrieval"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def add_document_to_db(chunks, filename):
    """Add document chunks to ChromaDB"""
    documents = []
    metadatas = []
    ids = []
    
    for i, chunk in enumerate(chunks):
        documents.append(chunk)
        metadatas.append({
            "filename": filename,
            "chunk_index": i,
            "total_chunks": len(chunks)
        })
        ids.append(f"{filename}_{i}_{uuid.uuid4()}")
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

def get_relevant_chunks(query, n_results=5):
    """Retrieve relevant document chunks from ChromaDB"""
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    except Exception as e:
        st.error(f"Query failed: {e}")
        return {"documents": [[]], "metadatas": [[]]}

def generate_response(query, context):
    """Generate a response using Gemini model with context"""
    prompt = f"""You are a helpful assistant that answers questions based on the provided document context. 

IMPORTANT INSTRUCTIONS:
- Only answer based on the information provided in the context below
- If the answer is not found in the context, respond with "I'm sorry, I don't have enough information in the provided document to answer that question."
- Do not make up or hallucinate information
- Be specific and cite relevant parts of the context when possible

Context from document:
{context}

Question: {query}

Answer:"""
    
    model = "gemini-2.0-flash-exp"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )
    
    response_text = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            response_text += chunk.text
    except Exception as e:
        return f"Error generating response: {e}"
    
    return response_text

def clear_database():
    """Clear all documents from the database"""
    try:
        chroma_client.delete_collection("document_chunks")
        global collection
        collection = chroma_client.create_collection("document_chunks")
        return True
    except:
        return False

# Streamlit UI
st.title("📄 Document RAG Assistant")
st.write("Upload a PDF document and ask questions based on its content")

# Sidebar for document management
with st.sidebar:
    st.header("Document Management")
    
    # Clear database button
    if st.button("🗑️ Clear Database", type="secondary"):
        if clear_database():
            st.success("Database cleared!")
            st.rerun()
        else:
            st.error("Failed to clear database")
    
    # Show collection info
    try:
        count = collection.count()
        st.info(f"📊 Document chunks in database: {count}")
    except:
        st.info("📊 Document chunks in database: 0")

# Document upload section
st.header("📤 Upload Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with st.spinner("Processing document..."):
        # Extract text from PDF
        text = extract_text_from_pdf(uploaded_file)
        
        if text.strip():
            # Split into chunks
            chunks = split_text_into_chunks(text)
            
            # Add to database
            add_document_to_db(chunks, uploaded_file.name)
            
            st.success(f"✅ Document '{uploaded_file.name}' processed successfully!")
            st.info(f"📝 Created {len(chunks)} text chunks")
            
            # Show document preview
            with st.expander("📋 Document Preview"):
                st.text_area("First 1000 characters:", text[:1000], height=200, disabled=True)
        else:
            st.error("❌ Could not extract text from the PDF. Please try a different file.")

# Query section
st.header("❓ Ask Questions")
user_query = st.text_input("Enter your question about the uploaded document(s):")

if st.button("🔍 Get Answer"):
    if user_query:
        if collection.count() > 0:
            with st.spinner("Searching for relevant information..."):
                # Get relevant chunks
                relevant_chunks = get_relevant_chunks(user_query)
                
                if relevant_chunks['documents'][0]:
                    # Prepare context from relevant chunks
                    context_parts = []
                    for doc, metadata in zip(relevant_chunks['documents'][0], relevant_chunks['metadatas'][0]):
                        context_parts.append(f"[From {metadata['filename']}]: {doc}")
                    
                    context = "\n\n".join(context_parts)
                    
                    # Generate response
                    with st.spinner("Generating answer..."):
                        response = generate_response(user_query, context)
                    
                    # Display results
                    st.subheader("🤖 Answer:")
                    st.write(response)
                    
                    # Show relevant chunks
                    with st.expander("📖 Relevant Document Sections"):
                        for i, (doc, metadata) in enumerate(zip(relevant_chunks['documents'][0], relevant_chunks['metadatas'][0])):
                            st.markdown(f"**Chunk {i+1} from {metadata['filename']}:**")
                            st.text_area(f"chunk_{i}", doc, height=100, disabled=True, key=f"chunk_{i}")
                            st.markdown("---")
                else:
                    st.warning("⚠️ No relevant information found in the uploaded documents.")
        else:
            st.warning("⚠️ Please upload a document first before asking questions.")
    else:
        st.warning("⚠️ Please enter a question.")

# Instructions
with st.expander("ℹ️ How to use"):
    st.markdown("""
    1. **Upload a PDF**: Click "Choose a PDF file" and select your document
    2. **Wait for processing**: The system will extract text and create searchable chunks
    3. **Ask questions**: Type your question in the text box and click "Get Answer"
    4. **Review results**: See the AI's answer and the relevant document sections used
    
    **Features:**
    - ✅ Only answers based on document content
    - ✅ Says "I don't know" when information isn't available
    - ✅ Shows relevant source sections
    - ✅ Handles multiple documents
    - ✅ Clear database option to start fresh
    """)
