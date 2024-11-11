import streamlit as st
import os
from supabase import Client, create_client
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px



load_dotenv()

url: str  = os.environ.get("SUPABASE_URL")
print(url)
key: str  = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
print(key)

print("Scoring the Stuff")
print(st.session_state["transcription"])
print(st.session_state["score"])
print(st.session_state["f0_range"])
print(st.session_state["content_score"])
print(st.session_state["num_filler_words"])
print(st.session_state["eyes_on_screen"])
print(st.session_state["f0_average"])
# eye_on_screen = get_eye_on_screen()
# transcript = get_transcript_for_score()
# no_of_filler_words = get_number_of_filler_words_score()
# words_spoken_clearly = get_words_spoken_clearly_score()
# content_score = get_content_score()

st.session_state["score"] = (
    5* st.session_state["f0_range"] + 30 * st.session_state["content_score"] + 3 * st.session_state["f0_average"]
    - 3 * st.session_state["num_filler_words"] + st.session_state["eyes_on_screen"])

insert_response = (supabase.table("BetterSpeak").upsert({
    "transcription": st.session_state["transcription"],
    "score": st.session_state["score"],
    "f0_range": st.session_state["f0_range"],
    "content_score": st.session_state["content_score"],
    "num_filler_words": st.session_state["num_filler_words"],
    "eyes_on_screen": st.session_state["eyes_on_screen"],
    "f0_average": st.session_state["f0_average"]
    }).execute())
response = supabase.table("BetterSpeak").select("*").execute()
df = pd.DataFrame(response.data)

print(response)
st.title("Score")

st.markdown("---")
col1, col2 = st.columns(2)

# Line chart for scores over time
fig_score = px.line(df, x='index', y='score', title='Score Over Time', markers=True)
st.plotly_chart(fig_score)

# Bar chart for f0_range
fig_f0_range = px.bar(df, x='index', y='f0_range', title='F0 Range by Index')
st.plotly_chart(fig_f0_range)

# Bar chart for content_score
fig_content_score = px.bar(df, x='index', y='content_score', title='Content Score by Index', color='content_score')
st.plotly_chart(fig_content_score)

# Bar chart for num_filler_words
fig_num_filler_words = px.bar(df, x='index', y='num_filler_words', title='Number of Filler Words by Index')
st.plotly_chart(fig_num_filler_words)

# Line chart for eyes_on_screen
fig_eyes_on_screen = px.line(df, x='index', y='eyes_on_screen', title='Eyes On Screen Over Time', markers=True)
st.plotly_chart(fig_eyes_on_screen)

# Display the raw data
st.subheader('Data')
st.write(df)

# Run Streamlit app
# streamlit run app.py
