import pandas as pd

def load_table(file_path):
    """
    Carga un archivo CSV como tabla.
    """
    return pd.read_csv(file_path)

def get_min_rod_diameter(force, rod_table):
    """
    Obtiene el diámetro mínimo del vástago según la fuerza requerida.
    """
    for _, row in rod_table.iterrows():
        if force <= row["Fuerza Máxima (kN)"]:
            return row["Diámetro Mínimo (mm)"]
    raise ValueError("Fuerza fuera de rango en la tabla de vástagos.")

def get_min_bore_diameter(force, pressure, bore_table):
    """
    Obtiene el diámetro interno mínimo de la camisa según la fuerza y presión.
    """
    for _, row in bore_table.iterrows():
        if force <= row["Fuerza Máxima (kN)"] and pressure <= row["Presión Máxima (bar)"]:
            return row["Diámetro Interno (mm)"]
    raise ValueError("Fuerza o presión fuera de rango en la tabla de camisas.")
