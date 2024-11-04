import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2
from matplotlib import pyplot as plt 

st.set_page_config(
    page_title="BetterSpeaker",
    page_icon="🏠",
    layout="wide")
st.markdown("<h1 style='text-align: center;'>BetterSpeaker</h1>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center;'> Make your voice heard</h4>", unsafe_allow_html=True)

record_page = st.Page("pages/recorder.py",title="Record Audio",icon="🎤")
analysis_page = st.Page("pages/analysis.py",title="Analysis",icon="📊")

pg = st.navigation([record_page,analysis_page])

pg.run()


