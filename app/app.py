import streamlit as st
import os
# import pandas
from utils.video_processing import process_video, save_processed_video_data
from utils.prepare_vectordb import get_vectorstore
from utils.session_state import initialize_session_state_variables
from utils.chatbot import chat
from utils.web_scraper import scrape_website
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ChatApp:
    def __init__(self):
        if not os.path.exists("docs"):
            os.makedirs("docs")
        if not os.path.exists("videos"):
            os.makedirs("videos")
        
        st.set_page_config(page_title="Chat with PDFS :books:")
        st.title("Chat with PDFS :books:")
        initialize_session_state_variables(st)
        self.docs_files = st.session_state.processed_documents

    def get_text_based_response(self, user_input):
        from utils.chatbot import get_text_response
        return get_text_response(user_input)

    def process_video(self, video_file):
        # Save video to a temporary file
        temp_video_path = os.path.join("videos", video_file.name)
        with open(temp_video_path, "wb") as f:
            f.write(video_file.read())

        # Process the video
        text_content, transcription_content = process_video(temp_video_path)
        
        # Save the extracted text and transcription
        save_processed_video_data(text_content, transcription_content)
        
        st.success("Video processed successfully!")

    def run(self):
        upload_docs = os.listdir("docs")
        with st.sidebar:
            st.subheader("Your documents")
            if upload_docs:
                st.write("Uploaded Documents:")
                st.text(", ".join(upload_docs))
            else:
                st.info("No documents uploaded yet.")

            st.subheader("Upload PDF documents")
            pdf_docs = st.file_uploader("Select a PDF document and click on 'Process'", type=['pdf'], accept_multiple_files=True)
            if pdf_docs:
                # Save and process PDFs
                pdf_file_paths = [f.name for f in pdf_docs]
                for pdf_file in pdf_docs:
                    with open(os.path.join("docs", pdf_file.name), "wb") as f:
                        f.write(pdf_file.read())
                get_vectorstore(pdf_file_paths, from_session_state=False)
            
            st.subheader("Scrape Website")
            url = st.text_input("Enter website URL:")
            if st.button("Scrape Website"):
                if url:
                    scraped_text = scrape_website(url)
                    if scraped_text and "Error" not in scraped_text:
                        with open("docs/scraped_website.txt", "w") as f:
                            f.write(scraped_text)
                        st.success("Website scraped and content saved!")
                    else:
                        st.error("Please enter a valid URL.")
                    get_vectorstore(upload_docs + ["scraped_website.txt"], scraped_text=scraped_text, from_session_state=False)
            
            st.subheader("Upload Video")
            video_file = st.file_uploader("Select a video file", type=['mp4', 'avi', 'mov'])
            if video_file:
                self.process_video(video_file)
            
            # st.subheader("Direct Text Input")
            # user_input = st.text_input("Enter text prompt:")
            # if st.button("Submit"):
            #     if user_input:
            #         response = self.get_text_based_response(user_input)
            #         st.write(f"Response: {response}")

        if self.docs_files or st.session_state.uploaded_pdfs or os.path.exists("docs/scraped_website.txt") or os.path.exists("docs/video_text.txt"):
            if len(upload_docs) > st.session_state.previous_upload_docs_length:
                st.session_state.vectordb = get_vectorstore(upload_docs + ["scraped_website.txt", "video_text.txt"], from_session_state=True)
                st.session_state.previous_upload_docs_length = len(upload_docs)
            st.session_state.chat_history = chat(st.session_state.chat_history, st.session_state.vectordb)
        if len(upload_docs) > st.session_state.previous_upload_docs_length or os.path.exists("docs/scraped_website.txt") or os.path.exists("docs/video_text.txt"):
            upload_docs.append("scraped_website.txt")
            upload_docs.append("video_text.txt")  # Ensure video data is included
            persist_directory = "Vector_DB - Documents"
            st.session_state.vectordb = get_vectorstore(upload_docs, from_session_state=True)
            st.session_state.previous_upload_docs_length = len(upload_docs)

        if not self.docs_files and not st.session_state.uploaded_pdfs and not os.path.exists("docs/scraped_website.txt") and not os.path.exists("docs/video_text.txt"):
            st.info("Upload a PDF file, scrape a website, or upload a video to interact with the content.")

if __name__ == "__main__":
    app = ChatApp()
    app.run()
