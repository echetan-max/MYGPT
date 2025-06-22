import streamlit as st
import requests

TOGETHER_API_KEY = "a677b7f43db92211bd652a7edbc39ec86bd47cfb15701868a9897de77c5ba8dd"
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

st.set_page_config(page_title="MYGPT", layout="centered")
st.title("MYGPT")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_NAME,
            "messages": st.session_state.messages,
            "temperature": 0.7,
            "max_tokens": 512,
            "top_p": 0.95
        }

        response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload)
        reply = response.json()["choices"][0]["message"]["content"]
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
