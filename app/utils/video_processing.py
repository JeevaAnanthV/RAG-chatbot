import pytesseract
import speech_recognition as sr
from moviepy.editor import VideoFileClip
import tempfile
import os

# Set the path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'"C:\Program Files\Tesseract-OCR\tesseract.exe"'

def process_video(video_file_path):
    """
    Process the video file to extract text and transcribe speech.

    Parameters:
    - video_file_path (str): Path to the video file

    Returns:
    - tuple: (text_content, transcription_content)
    """
    # Extract text and transcribe speech
    text_content = ""
    transcription_content = ""

    # Load the video and process frames
    video_clip = VideoFileClip(video_file_path)
    for frame in video_clip.iter_frames():
        text_content += pytesseract.image_to_string(frame)

    # Transcribe audio
    recognizer = sr.Recognizer()
    with sr.AudioFile(video_file_path) as source:
        audio = recognizer.record(source)
        transcription_content = recognizer.recognize_google(audio)

    return text_content, transcription_content

def save_processed_video_data(text_content, transcription_content, output_dir="docs"):
    """
    Save the extracted text and transcriptions to files.

    Parameters:
    - text_content (str): Text content extracted from video frames
    - transcription_content (str): Transcribed text from audio
    - output_dir (str): Directory to save the files
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save text content
    with open(os.path.join(output_dir, "video_text.txt"), "w") as text_file:
        text_file.write(text_content)

    # Save transcription content
    with open(os.path.join(output_dir, "video_transcription.txt"), "w") as transcription_file:
        transcription_file.write(transcription_content)
