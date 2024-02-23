import streamlit as st
from st_audiorec import st_audiorec
import tempfile
import speech_recognition as sr

# Initialize the speech recognizer
r = sr.Recognizer()

# Function to convert audio file to text
def convert_audio_to_text(audio_file_path):
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = r.record(source)  # Record the audio
            text = r.recognize_google(audio)
            return text.lower()  # Ensure lowercase for better input consistency
    except sr.UnknownValueError:
        st.write("Could not understand audio")
        return None
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except Exception as e:
        st.write(f"An error occurred: {e}")
        return None

# Streamlit app
st.title("Voice to Text Converter")

# Create a placeholder to store the recorded audio data
audio_placeholder = st.empty()

# Add an instance of the audio recorder to your streamlit app's code
audio_data = st_audiorec()

# Display the recorded audio
audio_placeholder.audio(audio_data, format="audio/wav")

if st.button("Convert to Text"):
    # Save the recorded audio data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
        temp_audio_file.write(audio_data)
        temp_audio_path = temp_audio_file.name

    # Convert the recorded audio file to text
    voice_text = convert_audio_to_text(temp_audio_path)
    if voice_text:
        st.write(f"You said: {voice_text}")
