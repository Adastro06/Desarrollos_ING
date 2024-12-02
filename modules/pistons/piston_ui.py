import streamlit as st
from modules.pistons.piston_calc import piston_design
from modules.standards import load_table

def piston_app():
    st.title("Diseño de Pistones Hidráulicos")
    st.markdown("Diseña automáticamente según las normas NFPA y propiedades del material.")

    # Cargar tablas
    try:
        rod_table = load_table("C:\\Users\\enriq\\Documents\\Programacion\\Herramienta de ingenieria\\data\\vastagos.csv")
        bore_table = load_table("C:\\Users\\enriq\\Documents\\Programacion\\Herramienta de ingenieria\\data\\camisas.csv")
        material_properties = load_table("C:\\Users\\enriq\\Documents\\Programacion\\Herramienta de ingenieria\\data\\Pistones_Cilindros_Materiales.csv").to_dict(orient="records")
    except Exception as e:
        st.error(f"Error al cargar las tablas: {str(e)}")
        return

    # Seleccionar material
    material_names = [mat["Material"] for mat in material_properties]
    selected_material = st.selectbox("Selecciona el material", material_names)

    # Entradas del usuario
    force = st.number_input("Fuerza requerida (kN)", min_value=1.0, step=0.1)
    length = st.number_input("Carrera (mm)", min_value=10.0, step=1.0)
    calc_pressure = st.checkbox("Calcular la presión de trabajo automáticamente")
    pressure = None

    if not calc_pressure:
        pressure = st.number_input("Presión de trabajo (bar)", min_value=10.0, step=1.0)

    if st.button("Calcular"):
        try:
            material = next(mat for mat in material_properties if mat["Material"] == selected_material)
            design = piston_design(force, length, pressure if not calc_pressure else None, material, rod_table, bore_table)

            # Mostrar resultados en español
            st.subheader("Resultados del Diseño")
            st.write(f"Diámetro del Vástago: {design['Rod Diameter (mm)']:.2f} mm")
            st.write(f"Diámetro Interno de la Camisa: {design['Bore Diameter (mm)']:.2f} mm")
            st.write(f"Presión de Trabajo: {design['Pressure (bar)']:.2f} bar")
            st.write(f"Espesor de la Camisa: {design['Thickness (mm)']:.2f} mm")
            st.write(f"Factor de Seguridad: {design['Factor of Safety']:.2f}")
            st.write(f"Volumen del Cilindro: {design['Volume (m³)']:.6f} m³")
            st.write(f"Peso Total: {design['Weight (kg)']:.2f} kg")
            st.write(f"Costo del Material: ${design['Cost ($)']:.2f} USD")
        except ValueError as e:
            st.error(str(e))


