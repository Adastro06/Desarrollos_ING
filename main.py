import streamlit as st
from modules.pistons.piston_ui import piston_app

st.sidebar.title("Mechanical Suite")
module = st.sidebar.selectbox("Selecciona un módulo", ["Pistones Hidráulicos"])

if module == "Pistones Hidráulicos":
    piston_app()
