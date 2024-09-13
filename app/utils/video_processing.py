import pytesseract
import speech_recognition as sr
from moviepy.editor import VideoFileClip
import os
import tempfile

# Set the path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def process_video(video_file_path):
    """
    Process the video file to extract text from video frames and transcribe speech from the audio.

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

    # Extract text from video frames
    for frame in video_clip.iter_frames():
        text_content += pytesseract.image_to_string(frame)

    # Save the extracted audio as a WAV file in a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        temp_audio_path = temp_audio_file.name
        video_clip.audio.write_audiofile(temp_audio_path, codec="pcm_s16le")

    # Transcribe audio using speech recognition
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(temp_audio_path) as source:
            audio = recognizer.record(source)
            transcription_content = recognizer.recognize_google(audio)
    except Exception as e:
        transcription_content = f"Error transcribing audio: {e}"

    # Clean up the temporary audio file
    os.remove(temp_audio_path)

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
