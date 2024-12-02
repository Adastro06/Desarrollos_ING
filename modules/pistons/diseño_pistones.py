import numpy as np
import streamlit as st

# Configuración inicial
st.title("Optimizador de Pistones Hidráulicos")
st.markdown("Encuentra la configuración óptima que cumpla con los requisitos de fuerza y factor de seguridad, minimizando el uso de material.")

# Entrada de datos
st.header("Requerimientos del Pistón")
col1, col2 = st.columns(2)

with col1:
    fuerza_requerida = st.number_input("Fuerza requerida (kN)", min_value=0.1, step=0.1)
    presion_maxima = st.number_input("Presión máxima (bar)", min_value=0.1, step=0.1)  # Sin límite máximo
    factor_seguridad_min = st.number_input("Factor de seguridad mínimo", min_value=1.0, step=0.1)

with col2:
    material = st.selectbox("Material del pistón", ["Acero SAE 1045", "Aluminio 6061-T6", "Acero inoxidable 316"])
    longitud_carrera = st.number_input("Longitud de la carrera (mm)", min_value=10.0, step=1.0)

# Propiedades del material
if material == "Acero SAE 1045":
    limite_elastico = 530  # MPa
    densidad = 7.85  # g/cm³
elif material == "Aluminio 6061-T6":
    limite_elastico = 276  # MPa
    densidad = 2.70  # g/cm³
elif material == "Acero inoxidable 316":
    limite_elastico = 290  # MPa
    densidad = 7.99  # g/cm³

# Rango de dimensiones a explorar
diametro_piston_range = np.arange(50, 500, 5)  # Diámetro del pistón (mm)
diametro_barra_range = np.arange(10, 300, 5)   # Diámetro de la barra (mm)

# Optimización
st.header("Resultados de Optimización")

if st.button("Optimizar"):
    presion_maxima_pa = presion_maxima * 1e5  # Convertir bar a Pascal
    mejor_configuracion = None
    menor_volumen = float('inf')

    for diametro_piston in diametro_piston_range:
        for diametro_barra in diametro_barra_range:
            if diametro_barra >= diametro_piston:  # La barra no puede ser más grande que el pistón
                continue
            
            # Cálculos de áreas
            area_piston = np.pi * (diametro_piston / 2)**2  # mm²
            area_barra = np.pi * (diametro_barra / 2)**2    # mm²
            fuerza_maxima = presion_maxima_pa * (area_piston - area_barra) / 1e6  # kN

            if fuerza_maxima < fuerza_requerida:  # No cumple con la fuerza requerida
                continue

            # Esfuerzo máximo y factor de seguridad
            esfuerzo_maximo = fuerza_maxima / (area_piston / 1e6)  # MPa
            factor_seguridad = limite_elastico / esfuerzo_maximo

            if factor_seguridad < factor_seguridad_min:  # No cumple con el factor de seguridad
                continue

            # Volumen del material (aproximación)
            volumen_piston = area_piston * longitud_carrera  # mm³
            volumen_barra = area_barra * longitud_carrera    # mm³
            volumen_total = volumen_piston + volumen_barra  # mm³

            # Comparar volúmenes para encontrar el menor
            if volumen_total < menor_volumen:
                menor_volumen = volumen_total
                mejor_configuracion = {
                    "diametro_piston": diametro_piston,
                    "diametro_barra": diametro_barra,
                    "fuerza_maxima": fuerza_maxima,
                    "factor_seguridad": factor_seguridad,
                    "volumen_total": volumen_total / 1e9,  # Convertir a m³
                }

    # Mostrar los resultados
    if mejor_configuracion:
        st.success("¡Configuración óptima encontrada!")
        st.write(f"Diámetro del pistón: {mejor_configuracion['diametro_piston']} mm")
        st.write(f"Diámetro de la barra: {mejor_configuracion['diametro_barra']} mm")
        st.write(f"Fuerza máxima generada: {mejor_configuracion['fuerza_maxima']:.2f} kN")
        st.write(f"Factor de seguridad: {mejor_configuracion['factor_seguridad']:.2f}")
        st.write(f"Volumen total del material: {mejor_configuracion['volumen_total']:.6f} m³")
    else:
        st.error("No se encontró ninguna configuración que cumpla con los requisitos.")
