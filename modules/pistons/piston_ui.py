import streamlit as st
from modules.pistons.piston_calc import optimize_piston
from utils.helpers import format_results

def piston_app():
    st.title("Pistones Hidráulicos")
    st.markdown("Optimiza configuraciones para pistones hidráulicos.")

    # Inputs del usuario
    fuerza_requerida = st.number_input("Fuerza requerida (kN)", min_value=0.1, step=0.1)
    presion_maxima = st.number_input("Presión máxima (bar)", min_value=50.0, step=1.0)
    factor_seguridad = st.number_input("Factor de seguridad mínimo", min_value=1.0, step=0.1)

    if st.button("Optimizar"):
        resultado = optimize_piston(fuerza_requerida, presion_maxima, factor_seguridad)
        st.write(format_results(resultado))