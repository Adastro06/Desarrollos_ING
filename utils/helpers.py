# helpers.py

def format_results(config):
    """
    Formatea los resultados para que se muestren de manera legible.
    """
    if not config:
        return "No se encontró una configuración válida."
    
    return (
        f"Diámetro del pistón: {config['diametro_piston']} mm\n"
        f"Diámetro de la barra: {config['diametro_barra']} mm\n"
        f"Fuerza máxima generada: {config['fuerza_maxima']:.2f} kN\n"
        f"Esfuerzo máximo: {config['esfuerzo_maximo']:.2f} MPa\n"
        f"Volumen total del material: {config['volumen_total']:.6f} m³"
    )
