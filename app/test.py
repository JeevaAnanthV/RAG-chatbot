import os
import pickle
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

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
                print(f"Vectorstore created and persisted to '{persist_directory}'.")
            
            return vectordb
        except Exception as e:
            print(f"Error creating or appending to vectorstore: {e}")
            return None
    
    print("Vectorstore creation skipped. Either no documents or an existing vectorstore is loaded.")
    return None

def read_scraped_text(file_path):
    """
    Read text content from a file with error handling for different encodings.

    Parameters:
    - file_path (str): Path to the file

    Returns:
    - str: Content of the file
    """
    encodings = ['utf-8', 'latin-1', 'utf-16']  # List of encodings to try

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError as e:
            print(f"Error reading file with encoding {encoding}: {e}")
        except Exception as e:
            print(f"Unexpected error reading file: {e}")
    
    raise ValueError("Unable to decode the file with the provided encodings.")

def similarity_search(vectordb, search_term):
    """
    Perform a similarity search on the vectorstore.

    Parameters:
    - vectordb (Chroma): The vectorstore object
    - search_term (str): Term to search in the vectorstore

    Returns:
    - None
    """
    try:
        search_results = vectordb.similarity_search(search_term, k=3)
        if search_results:
            print(f"Search term '{search_term}' found in the following documents:")
            for idx, result in enumerate(search_results, start=1):
                print(f"{idx}. {result.page_content[:300]}...")  # Display a snippet of the result
        else:
            print("Search term not found in the vectorstore.")
    except Exception as e:
        print(f"Error during similarity search: {e}")

def check_vectorstore_content(directory):
    """Print the content of the vectorstore directory for debugging."""
    if os.path.exists(directory):
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    try:
                        content = pickle.load(f)
                        print(f"Content from file {file}:")
                        print(content)
                    except Exception as e:
                        print(f"Error reading file {file}: {e}")
            else:
                print(f"{file_path} is not a file.")
    else:
        print(f"Directory {directory} does not exist.")

if __name__ == "__main__":
    # Define the path to the scraped text file
    scraped_file_path = "docs/scraped_website.txt"
    scraped_text = read_scraped_text(scraped_file_path)  # Read the text from the file

    # List of PDFs to process
    pdfs = ['LOR-JeevaV.pdf', 'Technical Assignment.pdf']

    # Get or create vectorstore with scraped text
    vectordb = get_vectorstore(pdfs, scraped_text=scraped_text)

    # Example search
    sample_term = "The college was established in 1984"
    if vectordb:
        similarity_search(vectordb, sample_term)
    
    # Check vectorstore contents
    check_vectorstore_content(r'L:/test4/RAG-chatbot/Vector_DB - Documents')