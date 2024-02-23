import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import numpy as np

# Initialize the speech recognizer
r = sr.Recognizer()

# Function to get the available audio devices
def get_available_audio_devices():
    return sd.query_devices()

# Function to record audio and convert it to text
def record_audio():
    available_devices = get_available_audio_devices()

    if not available_devices:
        st.write("No audio input devices found.")
        return None

    selected_device = st.selectbox("Select Audio Device", [device['name'] for device in available_devices])

    try:
        with sd.InputStream(device=available_devices[selected_device]['device'], channels=1, callback=callback):
            st.write("Speak...")
            st.button("Stop Recording")  # Display a button to stop recording
            st.write("Recording...")
            st.experimental_rerun()  # Rerun the app to stop recording when the button is clicked
    except Exception as e:
        st.write(f"An error occurred: {e}")
        return None

# Callback function for recording
def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    st.session_state.audio_data = np.concatenate([st.session_state.get("audio_data", []), indata.flatten()])
    
# Streamlit app
st.title("Voice to Text Converter")

# If the "Record Audio" button is clicked
if st.button("Record Audio"):
    # Record the audio and convert it to text
    st.session_state.audio_data = []  # Initialize audio data
    record_audio()

    # Process the recorded audio data
    if st.session_state.audio_data:
        audio_data = np.array(st.session_state.audio_data)
        text = recognize_audio(audio_data)
        if text:
            st.write(f"You said: {text}")
