from modules.standards import get_min_rod_diameter, get_min_bore_diameter

def piston_design(force, length, pressure, material_properties, rod_table, bore_table):
    """
    Calcula el diseño inicial del cilindro usando las tablas de normas.
    Si no se proporciona presión, se calcula automáticamente.
    """
    # Propiedades del material
    stress_admissible = material_properties["Esfuerzo Admisible (MPa)"] * 1e6  # Pa
    density = material_properties["Densidad (g/cm³)"] * 1e3  # kg/m³
    cost_per_unit_volume = material_properties["Costo por Unidad ($/cm³)"]

    # Diámetros mínimos según las tablas
    min_rod_diameter = get_min_rod_diameter(force, rod_table)
    min_bore_diameter = bore_table.loc[bore_table["Fuerza Máxima (kN)"] >= force, "Diámetro Interno (mm)"].iloc[0]

    # Si no se proporciona presión, calcularla automáticamente
    if pressure is None:
        area_bore = 3.1416 * (min_bore_diameter / 1000)**2 / 4  # Área en m²
        pressure = force * 1000 / area_bore  # Presión en Pa (fuerza en N)

    # Validar presión contra la máxima permitida
    max_pressure = bore_table.loc[bore_table["Diámetro Interno (mm)"] == min_bore_diameter, "Presión Máxima (bar)"].values[0] * 1e5
    if pressure > max_pressure:
        raise ValueError(f"La presión calculada ({pressure / 1e5:.2f} bar) excede el límite permitido de {max_pressure / 1e5:.2f} bar.")

    # Cálculo del espesor de la camisa
    t = (pressure * min_bore_diameter) / (2 * (stress_admissible - pressure))
    if t <= 0:
        raise ValueError("El espesor calculado no es válido.")

    # Cálculo del factor de seguridad
    stress_max = (pressure * min_bore_diameter) / (2 * t)
    fs = stress_admissible / stress_max

    # Cálculo del volumen y peso del cilindro
    outer_diameter = min_bore_diameter + 2 * t
    volume_cylinder = 3.1416 * ((outer_diameter**2 - min_bore_diameter**2) / 4) * (length / 1000)
    weight = volume_cylinder * density
    cost = volume_cylinder * cost_per_unit_volume

    return {
        "Rod Diameter (mm)": min_rod_diameter,
        "Bore Diameter (mm)": min_bore_diameter,
        "Pressure (bar)": pressure / 1e5,  # Convertir a bar
        "Thickness (mm)": t,
        "Factor of Safety": fs,
        "Volume (m³)": volume_cylinder,
        "Weight (kg)": weight,
        "Cost ($)": cost,
    }
