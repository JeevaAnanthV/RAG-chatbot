from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import os
def extract_pdf_text(pdfs):
    """
    Extract text from PDF documents

    Parameters:
    - pdfs (list): List of PDF documents

    Returns:
    - docs: List of text extracted from PDF documents
    """
    docs = []
    for pdf in pdfs:
        pdf_path = os.path.join("docs", pdf)
        docs.extend(PyPDFLoader(pdf_path).load())
    return docs

def get_text_chunks(docs):
    """
    Split text into chunks

    Parameters:
    - docs (list): List of text documents

    Returns:
    - chunks: List of text chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=8000, chunk_overlap=800, separators=["\n\n", "\n", " ", ""])
    chunks = text_splitter.split_documents(docs)
    return chunks

def get_vectorstore(pdfs, scraped_text=None, from_session_state=False):
    """
    Create or retrieve a vectorstore from PDF documents and scraped content.

    Parameters:
    - pdfs (list): List of PDF file paths
    - scraped_text (str, optional): Scraped text content to add to vectorstore
    - from_session_state (bool): Flag to indicate if the vectorstore should be loaded from session state

    Returns:
    - Chroma: The vectorstore object
    """
    load_dotenv()
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Set the correct path for the vectorstore directory
    persist_directory = "L:/test4/RAG-chatbot/Vector_DB - Documents"
    
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)  # Ensure the directory is created

    # Retrieve vectorstore from existing one
    if from_session_state and os.path.exists(persist_directory):
        try:
            vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
            return vectordb
        except Exception as e:
            print(f"Error loading vectorstore from '{persist_directory}': {e}")
            return None
    
    # Create or update vectorstore
    elif not from_session_state:
        docs = extract_pdf_text(pdfs)  # Extract text from PDFs
        
        # Directly add scraped text as a document if provided
        if scraped_text:
            docs.append(scraped_text)  # Ensure scraped text is added as a separate document

        # Ensure documents are processed
        if not docs:
            print("No documents found for creating vectorstore.")
            return None

        chunks = get_text_chunks(docs)  # Chunk the documents
        
        try:
            if os.path.exists(persist_directory) and len(chunks) > 0:
                vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
                vectordb.add_documents(documents=chunks)  # Append new data to the existing vectorstore
                vectordb.persist()  # Persist changes
            else:
                vectordb = Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=persist_directory)
                vectordb.persist()  # Ensure persistence
            
            return vectordb
        except Exception as e:
            print(f"Error creating or appending to vectorstore: {e}")
            return None
    
    return None
