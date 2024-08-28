import streamlit as st

from longchain.schema import HumanMessage, SystemMessage, AIMessage
from longchain.chat_model import ChatOpenAI

st.set_page_config(page_title="Conversation Q&A Chatbot")
st.header("Hey,Let's chat")

from dotenv import load_dotenv
load_dotenv()
import os

chat=ChatOpenAI(temperature=0.5)
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] =SystemMessage(content="You are activat")

def get_openai_response(question):
    st.session_state['flowmessages'].append(HumanMessage(content=question))
    answer=chat(st.session_state['flowmessages'])
    st.session_state['flowmessages'].append(AIMessage(content=answer.content))
    return answer.content

input_text=st.text_input("Input: ",key="input")


submit=st.button("Ask the questions")

if submit:
    response=get_openai_response(input_text)
    st.subheader("The Response is")
    st.write(response)
