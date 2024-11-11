import streamlit as st
import requests
import os
from dotenv import load_dotenv

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

#AI Modules
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from scripts.analyze_audio import AudioAnalyzer

from gaze_tracking.example import run_eye_tracking

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



        



st.sidebar.markdown("## Analysis")
st.sidebar.write('This section is where you analyze your recorded video and note any improvements to your speech.')


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
        width: 450px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 450px;
        margin-left: -450px;
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
# if not video_file_buffer:
#     if use_webcam:
#         vid = cv2.VideoCapture(0)
#     else:
#         vid = cv2.VideoCapture(DEMO_VIDEO)
#         tffile.name = DEMO_VIDEO
# else:
#     tffile.write(video_file_buffer.read())
#     vid = cv2.VideoCapture(tffile.name)

# width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps_input = int(vid.get(cv2.CAP_PROP_FPS))

#Recording Part

    
st.sidebar.text('Input Video')
st.sidebar.video(tffile.name)




st.markdown("<hr/>",unsafe_allow_html=True)

Analyzer = AudioAnalyzer("assets/output.wav")
col1, col2 = st.columns(2)

with col1:
    Analyzer.get_energy_db()
with col2:
    st.session_state["f0_average"], st.session_state["f0_range"] = Analyzer.get_fundamental_frequency()
    Analyzer.get_waveform()

print("Running Eye Tracking")
run_eye_tracking()
# img_file_buffer = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
# if img_file_buffer is not None:
#     image = np.array(Image.open(img_file_buffer))
    
# else:
#     demo_image = DEMO_IMAGE
#     image  = np.array(Image.open(demo_image))

# st.sidebar.text('Input Image')
# st.sidebar.image(image)

# face_count = 0

#This should not be commented out
# total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

# # Dashbaord
# with mp_face_mesh.FaceMesh(
# static_image_mode=False,
# max_num_faces = max_faces, 
# min_detection_confidence = detection_confidence,
# min_tracking_confidence = tracking_confidence
# ) as face_mesh:
#     prevTime = 0
    
#     while vid.isOpened():

#         i += 1
#         ret, frame = vid.read()
        
#         if not ret:
#             continue
        
#         frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
#         results = face_mesh.process(frame)
#         frame.flags.writeable = True
#         frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

#         face_count = 0
#         if results.multi_face_landmarks:
            
#             ##Face Landmark Drawing
#             for face_landmarks in results.multi_face_landmarks:
#                 face_count += 1
                
#                 mp_drawing.draw_landmarks(
#                     image = frame,
#                     landmark_list=face_landmarks,
#                     connections = mp_face_mesh.FACEMESH_TESSELATION,
#                     landmark_drawing_spec=drawing_spec,
#                     connection_drawing_spec=drawing_spec)
#         currTime = time.time()
#         fps = 1/(currTime-prevTime)
#         prevTime = currTime
        
#         current_frame = int(vid.get(cv2.CAP_PROP_POS_FRAMES))
        
#         if current_frame == total_frames - 1:
#             print("End of video")
#             break
#         kpi1_text.write(f"<h1 style='text-align: center;'>{int(fps)}</h1>", unsafe_allow_html=True)
#         kpi2_text.write(f"<h1 style='text-align: center;'>{face_count}</h1>", unsafe_allow_html=True)
#         kpi3_text.write(f"<h1 style='text-align: center;'>{width}</h1>", unsafe_allow_html=True)
        
#         frame = cv2.resize(frame,(0,0),fx=0.8,fy=0.8) 
#         frame = image_resize(image = frame, width = 640)
#         stframe.image(frame, channels = 'BGR', use_column_width=True)



# st.video("https://youtu.be/La5zCcBmOuk?list=TLPQMDMxMTIwMjSryh_Ho62WWw")


#audio analysis
audio = "assets/output.wav"

y, sr = librosa.load(audio)


