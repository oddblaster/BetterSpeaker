import streamlit as st
import requests

#Audio Libraries
import librosa


#Data Science Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Computer vision libraries
import mediapipe as mp
from PIL import Image
import time
import tempfile
import cv2


#Filler Words
filler_words = {
    # Common single-word fillers
    "uh", "um", "er", "like", "well", "so", "right", "okay", "yeah", "yep", 
    "just", "actually", "literally", "basically", "totally", "honestly", 
    "truthfully", "obviously", "guess",
    
    # Multi-word fillers and phrases
    "you know", "i mean", "sort of", "kind of", "you see", "if you will", 
    "in a way", "in a sense", "to be honest", "to tell you the truth", 
    "at the end of the day", "the thing is", "for what it’s worth", 
    "as a matter of fact", "in my opinion",
    
    # Transitional fillers
    "anyway", "by the way", "in other words", "moving on", 
    "you know what I mean",
    
    # Hedging words
    "maybe", "perhaps", "probably", "supposedly", "possibly", "potentially",
    
    # Thinking fillers
    "let me see", "let’s see", "hold on", "hang on", "how should I put this", 
    "give me a second"
}

# Image Resize Function
@st.cache_data()
def image_resize(image, width=None, height=None, inter =cv2.INTER_AREA):
    dim = None
    (h,w) = image.shape[:2]
    
    if width is None and height is None:
        return image
    
    if width is None:
        r= width/float(w)
        dim = (int(w*r),height)
    
    else:
        r = width/float(w)
        dim = (width,int(h*r))
    
    #resize the image
    resized =cv2.resize(image,dim,interpolation=inter)
    
    return resized
def audio_analysis():
    #Audio Buffers, y: audio time series which is a NumPy array representing the audio signal
    #sr: sampling rate
    y, sr = librosa.load("assets/output.wav")

    
    col1, col2, col3 = st.columns(3)

    with col1:
        
        st.subheader("Volume")
        
        fig, ax = plt.subplots()
        librosa.display.waveshow(y=y, sr=sr, ax=ax)

        y_harmonic, y_percussive = librosa.effects.hpss(y)
        
        

        with st.expander("Audio Waveform"):
            st.pyplot(fig)
    with col2:
        st.subheader("Filler Words")
    with col3:
        st.subheader("Pauses")
        



st.sidebar.markdown("## Analysis")
st.sidebar.write('This section is where you analyze your recorded video and note any improvements to your speech.')
st.fragment(func=audio_analysis())


mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

DEMO_IMAGE = "assets/demo.jpg"
DEMO_VIDEO = "assets/demo.mp4"


st.sidebar.markdown('---')



#Sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 350px;
        margin-left: -350px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



## Parameters for Face Detection
st.sidebar.subheader('Parameters')
max_faces = st.sidebar.number_input("Maximum Number of Faces", value=2, min_value=1)
drawing_spec = mp_drawing.DrawingSpec(thickness =2, circle_radius=1)
detection_confidence = st.sidebar.slider("Min Detection Confidence", min_value=0.0,max_value=1.0,value=0.5)
tracking_confidence = st.sidebar.slider("Min Tracking Confidence", min_value=0.0,max_value=1.0,value=0.5)


record = st.sidebar.checkbox("Record")

if record:
    st.checkbox("Recording", value=True)
    
use_webcam = st.sidebar.button('Use Webcam')
stframe = st.empty()
video_file_buffer = st.sidebar.file_uploader("Upload a video", type=["mp4", "mov", "avi", "asf", "mkv", "m4v", "webm"])
tffile = tempfile.NamedTemporaryFile(delete=False)

## Get the input video here
if not video_file_buffer:
    if use_webcam:
        vid = cv2.VideoCapture(0)
    else:
        vid = cv2.VideoCapture(DEMO_VIDEO)
        tffile.name = DEMO_VIDEO
else:
    tffile.write(video_file_buffer.read())
    vid = cv2.VideoCapture(tffile.name)

width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps_input = int(vid.get(cv2.CAP_PROP_FPS))

#Recording Part
codec =cv2.VideoWriter_fourcc('m','p','4','v')
out = cv2.VideoWriter('assets/output.mp4', codec, fps_input, (width, height))
    
st.sidebar.text('Input Video')
st.sidebar.video(tffile.name)

fps = 0
i = 0
drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.markdown("**Frame Rate**")
    kpi1_text = st.markdown("0")
with kpi2:
    st.markdown("**Detected Faces**")
    kpi2_text = st.markdown("0")
with kpi3:
    st.markdown("**Image Width**")
    kpi3_text = st.markdown("0")

st.markdown("<hr/>",unsafe_allow_html=True)
# img_file_buffer = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
# if img_file_buffer is not None:
#     image = np.array(Image.open(img_file_buffer))
    
# else:
#     demo_image = DEMO_IMAGE
#     image  = np.array(Image.open(demo_image))

# st.sidebar.text('Input Image')
# st.sidebar.image(image)

# face_count = 0

total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

# Dashbaord
with mp_face_mesh.FaceMesh(
static_image_mode=False,
max_num_faces = max_faces, 
min_detection_confidence = detection_confidence,
min_tracking_confidence = tracking_confidence
) as face_mesh:
    prevTime = 0
    
    while vid.isOpened():

        i += 1
        ret, frame = vid.read()
        
        if not ret:
            continue
        
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame)
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

        face_count = 0
        if results.multi_face_landmarks:
            
            ##Face Landmark Drawing
            for face_landmarks in results.multi_face_landmarks:
                face_count += 1
                
                mp_drawing.draw_landmarks(
                    image = frame,
                    landmark_list=face_landmarks,
                    connections = mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=drawing_spec)
        currTime = time.time()
        fps = 1/(currTime-prevTime)
        prevTime = currTime
        
        current_frame = int(vid.get(cv2.CAP_PROP_POS_FRAMES))
        
        if current_frame == total_frames - 1:
            print("End of video")
            break

        kpi1_text.write(f"<h1 style='text-align: center;'>{int(fps)}</h1>", unsafe_allow_html=True)
        kpi2_text.write(f"<h1 style='text-align: center;'>{face_count}</h1>", unsafe_allow_html=True)
        kpi3_text.write(f"<h1 style='text-align: center;'>{width}</h1>", unsafe_allow_html=True)
        
        frame = cv2.resize(frame,(0,0),fx=0.8,fy=0.8) 
        frame = image_resize(image = frame, width = 640)
        stframe.image(frame, channels = 'BGR', use_column_width=True)



# st.video("https://youtu.be/La5zCcBmOuk?list=TLPQMDMxMTIwMjSryh_Ho62WWw")


#audio analysis
audio = "assets/output.wav"

y, sr = librosa.load(audio)




    
url = "https://integrate.api.nvidia.com/v1/chat/completions"

payload = {
    "model": "meta/llama-3.1-405b-instruct",
    "messages": [
        {
            "content": "I am going to Paris, what should I see?",
            "role": "user"
        }
    ],
    "temperature": 0.2,
    "top_p": 0.7,
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "string",
                "description": "string"
            }
        }
    ],
    "tool_choice": {
        "function": { "name": "string" },
        "type": "function"
    },
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "max_tokens": 1024,
    "stream": False,
    "stop": ["string"]
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)