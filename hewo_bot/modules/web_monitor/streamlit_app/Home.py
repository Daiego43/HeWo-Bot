import streamlit as st
import time

st.title("🤖 HeWo Web Monitor")
st.subheader("Welcome to HeWo's Web Monitor.")
st.write("This is a simple web monitor that controls a wide variety of HeWo's future capabilities.")

titulo = st.title("Title")
while True:
    titulo.text(f"{time.time()}")
    time.sleep(1)