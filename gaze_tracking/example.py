"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
import sys
print(sys.path)
from gaze_tracking import GazeTracking
import streamlit as st


def run_eye_tracking():
    st.session_state["eyes_on_screen"] = 0
    gaze = GazeTracking()
    vid = cv2.VideoCapture("assets/output.mp4")
    video = st.empty()
    
    number_of_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    
    for i in range(number_of_frames):
        # We get a new frame from the webcam
        ret, frame = vid.read()

        if not ret:
            break
        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"
            st.session_state["eyes_on_screen"] += 1
            

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        video.image(frame, channels="BGR")

        if cv2.waitKey(1) == 27:
            break
    
    vid.release()
    cv2.destroyAllWindows()