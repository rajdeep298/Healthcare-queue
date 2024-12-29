from datetime import datetime
import os
import speech_recognition as sr
import google.generativeai as genai
import shutil
# Configure the Gemini API with your API key
genai.configure(api_key="AIzaSyBvUC-yJ31i1N_4KpSITDC_x_XzbMWgzsk")


# Source and destination paths
source = r"C:\Users\rajde\Dropbox\PC (2)\Downloads\hackathon_audio.wav"
destination = r"D:\Healthcare-queue\Speech-to-Text\AudioFiles\Recording.wav"

# Copy the file
shutil.copy(source, destination)
print(f"File copied to {destination}")

# Function to summarize text using Google's Gemini API
def summarize_text_with_gemini(text):
    try:
        print("[INFO] Summarizing text using Google's Gemini API...")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Summarize the following text: {text}")
        summarized_text = response.text
        print(f"[INFO] Summarized Text: {summarized_text}")
        return summarized_text
    except Exception as e:
        print(f"[ERROR] Summarization failed: {e}")
        return text  # If summarization fails, return the original text


# Function to save text to a file with a timestamped name
def save_text_to_file(text, prefix="summary"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{prefix}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"[INFO] Text saved to file: {filename}")
    return filename


# Function to transcribe speech from a WAV file using speech_recognition
def transcribe_audio_file_with_speech_recognition(audio_file_path):
    recognizer = sr.Recognizer()
    try:
        print("[INFO] Transcribing audio file using speech_recognition...")
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)
            transcription = recognizer.recognize_google(audio)
            print(f"[INFO] Recognized text: {transcription}")
            return transcription
    except sr.UnknownValueError:
        print("[ERROR] Could not understand the audio.")
    except sr.RequestError as e:
        print(f"[ERROR] Error with the speech recognition service: {e}")
    except FileNotFoundError:
        print("[ERROR] Audio file not found.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    return ""


# Main function to process a WAV file and save its transcription and summary
def main():
    print("\n=== WAV to Text and Summarization App ===\n")

    # Static WAV file path
    wav_file_path = "AudioFiles/Recording.wav"

    # Transcribe the audio file
    transcription = transcribe_audio_file_with_speech_recognition(wav_file_path)

    if transcription:
        # Summarize the transcribed text
        summarized_text = summarize_text_with_gemini(transcription)

        # Save the summarized text to a file
        if summarized_text:
            save_text_to_file(summarized_text)

    print("[INFO] Processing complete.")


if __name__ == "__main__":
    main()
