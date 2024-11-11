import streamlit as st
import json
import asyncio
from scripts.transcribe import transcribe
from scripts.content_reviewer import generate_chat, generate_analysis


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

if "transcription" not in st.session_state:
    st.session_state["transcription"] = ""
if "words" not in st.session_state:
    st.session_state["words"] = ""
if "num_filler_words" not in st.session_state:
    st.session_state["num_filler_words"] = 0
if "words_spoken_clearly" not in st.session_state:
    st.session_state["words_spoken_clearly"] = []
if "analysis" not in st.session_state:
    st.session_state["analysis"] = ""
async def get_transcription_response():
    output_str, words = transcribe()
        
    return output_str, words

#Generate the response from the AI
def generate_response(transcription,prompt):
    print("Generating Chat Response from Transcription:" + transcription)
    response = generate_chat(transcription,prompt)
    
    return response

def get_number_of_filler_words(words):
    num_filler_words = 0
    for word in words:
        if word['word'] in filler_words:
            num_filler_words += 1
            
    st.session_state["num_filler_words"] = num_filler_words



def get_words_spoken_clearly(words):
    for word in words:
        if word["confidence"] > 0.5:
            st.session_state["words_spoken_clearly"].append(word)
def get_content_score():
    content_score = 0
    try:
        st.session_state["analysis"] = generate_analysis(st.session_state["transcription"])
    except:
        print("error")
    return int(st.session_state["analysis"].split("Overall score: ")[1].split("\n")[0])
def get_number_of_filler_words_score():
    return int(st.session_state["num_filler_words"]/len(st.session_state["transcription"].split(" ")))
def get_words_spoken_clearly_score():
    return int(len(st.session_state["words_spoken_clearly"])/ len(st.session_state["transcription"].split(" ")))
st.title("Text Analysis")

st.markdown("---")

if "process_audio" not in st.session_state:
    st.session_state["process_audio"] = False

if st.session_state["process_audio"] == False: 
    response = transcribe()
    try:
        st.session_state["transcription"], st.session_state["words"] = asyncio.run(get_transcription_response())
    except:
        print("error")
    
    st.session_state["process_audio"] = True

col1,col2 = st.columns(2)

with col1:
    st.markdown("**# of Filler Words:**")
    get_number_of_filler_words(st.session_state["words"])
    st.write(st.session_state["num_filler_words"])
with col2:
    st.markdown("**# of Words Spoken Clearly:**")
    get_words_spoken_clearly(st.session_state["words"])
    with st.container():
        st.write(len(st.session_state["words_spoken_clearly"]))
        st.write(st.session_state["words_spoken_clearly"])
    
st.markdown("---")
st.write(st.session_state["transcription"])
st.markdown("---")
st.title("Content Analysis")

st.session_state["analysis"] = generate_analysis(st.session_state["transcription"])

try:
    st.session_state["content_score"] = int(st.session_state["analysis"].split("Overall Score: ")[1].split("**")[0])    
    print(st.session_state["content_score"])    
except:
    print("error")
    st.session_state["content_score"] = 0  # Return None or a default value if extraction fails

st.write(st.session_state["analysis"])



with st.sidebar:
    st.markdown( """ <style> [data-testid="stSidebar"][aria-expanded="true"]{ min-width: 500px; max-width: 500px; } """, unsafe_allow_html=True)
    
    container = st.container(height = 500)
    #User input
    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How can we improve your speech?"}]
        
    prompt = st.chat_input("Type your message here...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
    with container:
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        


        #Generate a response if user responded to the last message     
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                response = ""
                with st.spinner("Thinking..."):
                    try:
                        user_input = st.session_state.messages[-1]['content']
                        print("st.session_state.messages[-1]",st.session_state.messages[-1]['content'], type(st.session_state.messages[-1]['content']))
                        print("Transcription:",st.session_state["transcription"])
                        response = generate_response(transcription=st.session_state["transcription"], prompt=user_input)
                        
                        container.write(response)
                    except Exception as e:
                        print(" Error: ", e)
                    
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) 
                

                
            


        