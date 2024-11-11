import wave 
import sys



#Audio Libraries
import pyaudio
import streamlit as st

#Video libraries
import cv2

#Audio Recorder
st.sidebar.markdown("## Audio Recorder")

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 30
WAVE_OUTPUT_FILENAME = "assets/output.wav"




#Gets the audio recording
def record():
    
    video_stream = st.empty()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        video_stream = st.empty()
    p = pyaudio.PyAudio()
    
    video = cv2.VideoCapture(0)
   
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('assets/output.mp4', fourcc, 30.0, (640,480))
    
    
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
        
        seconds = int((i* RECORD_SECONDS)/int(RATE / CHUNK * RECORD_SECONDS))
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




st.markdown("---")
#Streamlit Process

title = st.title("Recorder")

recording_bar = st.progress(0)
st.button("Record", key="rec", on_click=record)    




st.markdown("""
<style>
    .video_stream {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .title{
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>""",unsafe_allow_html=True)