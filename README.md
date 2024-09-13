# RAG - ChatBot: Retrieval Augmented Generation (RAG) chatbot using Google's Gemini-Pro model, Langchain, ChromaDB, and Streamlit
RAG - ChatBot: Retrieval Augmented Generation (RAG) Chatbot
Overview
The RAG-ChatBot is a Python-based application that allows users to chat with multiple PDF documents, scraped web content, or extracted video transcriptions. Users can ask questions in natural language, and the application provides relevant responses based on the content of the uploaded or scraped documents. This application utilizes Google's Gemini-Pro model, Langchain, ChromaDB, and Streamlit to generate accurate answers, ensuring responses are based solely on the provided content.

Key Features
Upload Documents: Upload PDF documents and interact with their content on the fly. No need to reload the app when adding new documents.
Offline Documents: Previously uploaded documents are retained, allowing users to chat with them immediately upon restarting the app.
Website Scraping: Users can provide URLs to scrape websites and interact with the extracted content.
Video Processing: Supports video uploads, processes the video to extract text (shown on the video) and transcribe speech. The extracted data is then stored for querying.
User-Friendly Interface: Crafted with Streamlit, the app has an intuitive interface where users can upload files or URLs and ask questions without needing complex configurations.
Chat History Retention: Retains up to 10 user questions and model responses, providing context for follow-up questions.
Source Verification: For each response, users can check the source of the information in the sidebar, ensuring transparency.
Persistent Vector Database: Uses ChromaDB to store vector embeddings, making future queries faster and more efficient.
How It Works
Project Schema
The app works by combining a Retriever component with a Generator component:

Upload PDF/URL/Video: Users can upload documents, provide URLs for web scraping, or upload video files.
Text Extraction and Processing:
PDFs: Extracts text and processes it.
URLs: Scrapes website content and processes the text.
Videos: Extracts text shown in the video and transcribes speech.
Text Chunking: Extracted text is chunked using RecursiveCharacterTextSplitter.
Embedding and Saving: Converts chunks to vectors using GoogleGenerativeAIEmbeddings and saves them in ChromaDB.
Similarity Matching: User queries are converted to vectors, and similarity searches are performed to find the most relevant chunks.
Response Generation: Relevant chunks and the query are passed to the LLM (Google's Gemini-Pro model) to generate responses.
Chat Continuation: As new data is added or more questions are asked, the system dynamically updates, providing a seamless user experience.
App Usage
Step-by-Step Instructions
Step 1: Create .env File
Clone this repository or download the files as a ZIP and extract them.

Navigate to the folder where the files README.md and requirements.txt are located. You will see the app folder as well.

Create a new text file and add the following content:

plaintext
Copy code
GOOGLE_API_KEY = "your_api_key"
Replace "your_api_key" with the actual API key you obtained from Google. Save this file as .env in the root folder of the project.

Step 2: Install Required Packages
Open a terminal in the project folder. You can do this by holding the Shift key and right-clicking in the folder, then selecting "Open Terminal."

Run the following command to install all the necessary dependencies:

bash
Copy code
pip install -r requirements.txt
Step 3: Run the App
In the same terminal, run the following command to start the app:

bash
Copy code
streamlit run app/app.py
A new window in your web browser should open automatically with the app ready to use.

To stop the app, simply press Ctrl + C in the terminal.

Detailed Functionalities
1. PDF Upload and Interaction
Upload PDF documents to chat with their content.
The app checks for a folder named docs and creates one if it doesn't exist. All PDFs are saved in this folder.
Extracted text is chunked and embedded using GoogleGenerativeAIEmbeddings before being stored in ChromaDB.
2. Web Scraping
Input a URL to scrape content from a website.
Scraped text is processed, chunked, embedded, and stored similarly to PDF documents.
The vector database (ChromaDB) is updated with the new content, allowing users to query the scraped data.
3. Video Processing
Upload video files for processing.
Extracts text displayed on the video and transcribes any spoken words.
The extracted and transcribed data is embedded and stored in ChromaDB for querying.
4. Chat History and Contextual Responses
Maintains up to 10 previous questions and answers to provide context for follow-up questions.
Responses are generated based on the user query, retrieved text chunks, and chat history.
5. Response Source Verification
Users can view the source of each response in the sidebar to ensure the answer is grounded in the uploaded documents, scraped data, or processed video content.
Repository Structure
app/: Contains the main application code.
app.py: Main Streamlit application file.
docs/: Stores uploaded PDF documents.
scraped_data/: Stores scraped website data.
video_data/: Stores extracted and transcribed video data.
Vector_DB - Documents/: Stores the vector database for PDF, scraped data, and video content.
requirements.txt: List of dependencies to be installed.
README.md: Project overview and setup guide (this file).
Contribution
Feel free to fork this repository and submit pull requests. We welcome all contributions that improve the app, add new features, or fix bugs.

License
This project is licensed under the MIT License. See the LICENSE file for more information.

Acknowledgments
Google Generative AI for their powerful embedding and LLM models.
Langchain for the integration and retrieval functionalities.
Streamlit for providing an intuitive web interface framework.
ChromaDB for its efficient vector database storage and retrieval capabilities.