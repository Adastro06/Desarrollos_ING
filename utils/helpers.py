import pandas as pd

def load_materials(file_path):
    """
    Carga los materiales desde un archivo CSV.
    Devuelve una lista de diccionarios con las propiedades de cada material.
    """
    try:
        materials_df = pd.read_csv(file_path)
        materials = materials_df.to_dict(orient="records")
        return materials
    except Exception as e:
        raise Exception(f"Error al cargar el archivo CSV: {str(e)}")
