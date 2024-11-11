import urllib.request
import json 
import subprocess

import os
from dotenv import load_dotenv
import re
from supabase import create_client, Client
import streamlit as st
full_transcript = ""
load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

#Define NVIDIA Command for transcription
command = [
    "python", "python-clients/scripts/asr/transcribe_file_offline.py",
    "--server", "grpc.nvcf.nvidia.com:443", "--use-ssl",
    "--metadata", "function-id", "1598d209-5e27-4d3c-8079-4751568b1081",
    "--metadata", "authorization", f"Bearer {NVIDIA_API_KEY}",
    "--language-code", "en-US",
    "--input-file", "assets/output.wav"
]

def parse_string_results(results):
    #Regular expression to match word series
    word_pattern = re.compile(r"words \{(.+?)\}",re.DOTALL)
    
    word_entries = word_pattern.findall(results)
    
    parsed_words = []
    for entry in word_entries:
        start_time = re.search(r"start_time: (\d+)",entry)
        end_time = re.search(r"end_time: (\d+)",entry)
        word = re.search(r"word: \"(.+?)\"",entry)
        confidence = re.search(r"confidence: (\d+\.\d+)",entry)
        
       # print(start_time, end_time, word, confidence)
        if start_time and end_time and word and confidence:
            parsed_words.append({
                "start_time": float(start_time.group(1))/1000.0,
                "end_time": float(end_time.group(1))/1000.0,
                "word": word.group(1),
                "confidence": float(confidence.group(1))
            })
    return parsed_words
def get_transcript(full_transcript):
    transcription = re.search(r"Final transcript: (.*)", full_transcript).group(1)
    return transcription
def transcribe():
    print("Transcribing...")
    #subprocess.run(["pip", "install", "protobuf==5.27.0", "grpcio==1.67.1", "grpcio-tools==1.67.1"])
    result = subprocess.run(command, capture_output=True,text=True)
    
    full_transcript = result.stdout  
    print("Standard output:", result.stdout)
    print("Standard error:", result.stderr)
    transcription = get_transcript(full_transcript)
    words = parse_string_results(full_transcript)
    print(transcription)
   
    print("Transcription complete")
    
    
    return transcription, words
def get_transcript_for_score():
    return full_transcript