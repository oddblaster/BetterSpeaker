import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2
from matplotlib import pyplot as plt 


if "transcription" not in st.session_state:
    st.session_state["transcription"] = ""

if "score" not in st.session_state:
    st.session_state["score"] = 0

if "f0_range" not in st.session_state:
    st.session_state["f0_range"] = 0

if "content_score" not in st.session_state:
    st.session_state["content_score"] = 0

if "num_filler_words" not in st.session_state:
    st.session_state["num_filler_words"] = 0

if "eyes_on_screen" not in st.session_state:
    st.session_state["eyes_on_screen"] = 0

if "f0_average" not in st.session_state:
    st.session_state["f0_average"] = 0
    
st.set_page_config(
    page_title="BetterSpeak",
    page_icon="🏠",
    layout="wide")
st.markdown("<h1 style='text-align: center;'>BetterSpeak</h1>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center;'> Make your voice heard</h4>", unsafe_allow_html=True)

record_page = st.Page("pages/recorder.py",title="Record Audio",icon="🎤")
analysis_page = st.Page("pages/analysis.py",title="Analysis",icon="📊")
text_analysis_page = st.Page("pages/text_analysis.py",title="Text Analysis",icon="📈")
score_page = st.Page("pages/score.py",title="Score",icon="🏆")

pg = st.navigation([record_page,analysis_page,text_analysis_page,score_page])

pg.run()


