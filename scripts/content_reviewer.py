from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain import hub
from langchain.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os
import getpass




load_dotenv()
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

# client = ChatNVIDIA(
#   model="meta/llama3-70b-instruct"
# )



#Retrieve and generate using the relevant snippets of the blog

# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

# rag_chain = (
#     {"context" : retriever | format_docs,
#     "question": RunnablePassthrough()}
#              | prompt
#              | client
#              | StrOutputParser()
# )
os.environ['NVIDIA_API_KEY'] = NVIDIA_API_KEY
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings


llm = ChatNVIDIA(
  model="meta/llama-3.1-405b-instruct",
  api_key=NVIDIA_API_KEY, 
  temperature=0.2,
  top_p=0.7,
  max_tokens=1024,
)

document_embedder = NVIDIAEmbeddings(mode="nvolveqa_40k", model_type="passage")
query_embedder = NVIDIAEmbeddings(mode="nvolveqa_40k", model_type="query")


loader = PyPDFLoader(
    "assets/ElevatorPitch.pdf"
)

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = FAISS.from_documents(documents=splits, embedding=document_embedder)


analyze_prompt = '''
        You are an expert in speech analysis and communication effectiveness with a thorough understanding of linguistic nuances, tone, clarity, and audience engagement.
        Score each task on a scale from 0 to 100 where 0 is poor and 100 is excellent for each of the sections, and at the end given an overall score based on the assessment. 
        Your task is to analyze the following script transcription and rate how well the context of the message is conveyed to the audience. You are required to provide a 
        detailed report that identifies and discusses the strengths and weaknesses of the speech. The analysis should cover the following aspects:

        1. **Content and Message Clarity**:
            - Is the main message of the speech clear and easy to understand?
            - Are the key points well-articulated and logically organized?
            - Is there any ambiguity or confusion in the message?

        2. **Audience Engagement**:
            - Does the speech capture and maintain the audience's attention?
            - Are there any elements, such as rhetorical questions, anecdotes, or humor, that enhance engagement?
            - How well does the speech connect with the audience's interests and concerns?

        3. **Tone and Emphasis**:
            - Is the tone of the speech appropriate for the context and audience?
            - How effectively does the speaker use emphasis to highlight important points?
            - Are there variations in tone that add dynamism to the speech?

        4. **Language and Style**:
            - Is the language used accessible and appropriate for the target audience?
            - Are there any stylistic elements, such as metaphors, analogies, or vivid descriptions, that enhance the speech?
            - Are there any instances of jargon or complex language that could hinder understanding?

        5. **Structure and Flow**:
            - Is the speech structured in a coherent, logical manner?
            - Are transitions between sections smooth and clear?
            - Does the speech have a strong opening and a compelling conclusion?

        Here is the script transcription for analysis:        

        ''' 
        
chat_prompt = '''
You are an expert in speech analysis and communication effectiveness with a thorough understanding of linguistic nuances, tone, clarity,
and audience engagement. You are an advisor that answers the questions the user asks.
'''


def get_chat_prompt():
    print("Generating Prompt Template for Chat")
    prompt_template = ChatPromptTemplate.from_messages(
        [("system",chat_prompt),
        ("user","{input}")]
    )
    return prompt_template

def get_analysis_prompt(transcription):
    print("Generating Prompt Template for Analysis")
    
    analysis_template = ChatPromptTemplate.from_template(analyze_prompt + transcription)
    #print(analyze_prompt + transcription)
    return analysis_template

def generate_chat(transcription,user_input):
    prompt_template = get_chat_prompt()
    print("Generating Chat Response")
    response = ""
    try:
        chain = prompt_template | llm | StrOutputParser()
        retriever = vectorstore.as_retriever()
        
        docs = "\n\\n".join(doc.page_content for doc in retriever.get_relevant_documents(user_input)) 
        
        augmented_input = f"Context: {docs}\n\n Transcription: {transcription}\n\nUser Input: {user_input}"
        print("augmented_input",augmented_input)
        response = chain.invoke({"input": augmented_input})
        print("response",response)
    except Exception as e:
        print(e)

    return response
def generate_analysis(transcription):
    print(transcription)
    chain = get_analysis_prompt(transcription) | llm | StrOutputParser()
    
    response = chain.invoke({"input": f"Perform the Analysis of the transcription:{transcription}"})
    

        
    print(response)
    return response

