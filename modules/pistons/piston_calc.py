# piston_calc.py
import numpy as np

def optimize_piston(fuerza_requerida, presion_maxima, factor_seguridad):
    diametro_piston_range = np.arange(150, 401, 10)
    diametro_barra_range = np.arange(50, 301, 10)
    presion_maxima_pa = presion_maxima * 1e5

    mejor_configuracion = None
    menor_volumen = float('inf')

    for dp in diametro_piston_range:
        for db in diametro_barra_range:
            if db >= dp:
                continue

            area_piston = np.pi * (dp / 2)**2
            area_barra = np.pi * (db / 2)**2
            fuerza_maxima = presion_maxima_pa * (area_piston - area_barra) / 1e6

            if fuerza_maxima < fuerza_requerida:
                continue

            esfuerzo_maximo = fuerza_maxima / (area_piston / 1e6)
            if esfuerzo_maximo > (530 / factor_seguridad):  # Límite elástico SAE 1045
                continue

            volumen_total = (area_piston + area_barra) * 1400  # Volumen estimado
            if volumen_total < menor_volumen:
                menor_volumen = volumen_total
                mejor_configuracion = {
                    "diametro_piston": dp,
                    "diametro_barra": db,
                    "fuerza_maxima": fuerza_maxima,
                    "esfuerzo_maximo": esfuerzo_maximo,
                    "volumen_total": volumen_total,
                }

    return mejor_configuracion
