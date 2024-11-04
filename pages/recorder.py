import wave 
import sys
import os
from dotenv import load_dotenv

#Audio Libraries
import pyaudio
import streamlit as st
import subprocess

#Video libraries
import cv2



load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

#Audio Recorder
st.sidebar.markdown("## Audio Recorder")

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 30720
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

#Define NVIDIA Command for transcription
command = [
    "python", "python-clients/scripts/asr/transcribe_file.py",
    "--server", "grpc.nvcf.nvidia.com:443",
    "--use-ssl",
    "--metadata", "function-id", "1598d209-5e27-4d3c-8079-4751568b1081",
    "--metadata", "authorization", f"Bearer {NVIDIA_API_KEY}",
    "--language-code", "en-US",
    "--input-file", "assets/output.wav"
]

#Gets the audio recording
def record_audio():
    p = pyaudio.PyAudio()
    
    video = cv2.VideoCapture(0)
   
     
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc,20.0, (640,480))
    

    video_stream = st.empty()
    
    
    if p.get_default_input_device_info() is None:
        st.error("No microphone found")
        st.stop()
        
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    
    print("Recording...")
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):

        ret, frame = video.read()
        if not ret:
            break
        video_stream.image(frame, channels="BGR")
        
        out.write(frame)
        data = stream.read(CHUNK)
        frames.append(data)
        seconds = (i* RATE/CHUNK)/int(RATE / CHUNK * RECORD_SECONDS)
        recording_bar.progress(i / int(RATE / CHUNK * RECORD_SECONDS),text=f"{seconds}/{RECORD_SECONDS}")
                
    
    print("Finished recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    video.release()
    out.release()
    cv2.destroyAllWindows()
    sound_file = wave.open("assets/output.wav","wb")
    sound_file.setnchannels(CHANNELS)
    sound_file.setsampwidth(p.get_sample_size(FORMAT))
    sound_file.setframerate(RATE)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()

    print("Transcribing...")
    result = subprocess.run(command, capture_output=True,text=True)
    st.write("Standard output:", result.stdout)
    
    st.write("Standard error:", result.stderr)
    print("Transcription complete")


st.markdown("---")
#Streamlit Process
st.title("Audio Recorder")
recording_bar = st.progress(0)
st.button("Record", key="rec", on_click=record_audio)
