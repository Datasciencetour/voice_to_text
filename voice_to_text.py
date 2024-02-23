import streamlit as st
import speech_recognition as sr

# Initialize the speech recognizer
r = sr.Recognizer()

# Function to record audio and convert it to text
def record_audio():
    with sr.Microphone() as source:
        st.write("Speak...")
        try:
            audio = r.listen(source, timeout=5)  # Set a timeout to handle no input gracefully
            text = r.recognize_google(audio)
            return text.lower()  # Ensure lowercase for better input consistency
        except sr.UnknownValueError:
            st.write("Could not understand audio")
            return None
        except sr.WaitTimeoutError:
            st.write("No audio detected within the timeout")
            return None
        except Exception as e:
            st.write(f"An error occurred: {e}")
            return None

# Streamlit app
st.title("Voice to Text Converter")

# If the "Record Audio" button is clicked
if st.button("Record Audio"):
    # Record the audio and convert it to text
    voice_text = record_audio()
    if voice_text:
        st.write(f"You said: {voice_text}")
