import streamlit as st
from modules.pistons.piston_ui import piston_app

# Selección del módulo
st.sidebar.title("Mechanical Suite")
module = st.sidebar.selectbox(
    "Selecciona un módulo",
    ["Pistones Hidráulicos", "Válvulas", "Vigas Estructurales"]
)

# Cargar el módulo correspondiente
if module == "Pistones Hidráulicos":
    piston_app()
elif module == "Válvulas":
    st.write("Módulo de válvulas en desarrollo.")
elif module == "Vigas Estructurales":
    st.write("Módulo de vigas en desarrollo.")
