import streamlit as st

file = st.file_uploader('select a file to upload pls 🤖', type = ["png","jpeg", 'webp', 'jpg'])

if file is not None:
    st.image(file)