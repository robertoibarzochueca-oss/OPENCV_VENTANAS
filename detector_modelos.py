import cv2
import numpy as np
import os
import json

# ==========================================
# CARPETAS
# ==========================================

CARPETA_BASE = "BASE"
CARPETA_RECORTES = "recortes"

# ==========================================
# FUNCION PARA COMPARAR FORMAS
# ==========================================

def comparar_imagenes(img1, img2):

    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))

    gris1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gris2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    _, th1 = cv2.threshold(gris1, 200, 255, cv2.THRESH_BINARY_INV)
    _, th2 = cv2.threshold(gris2, 200, 255, cv2.THRESH_BINARY_INV)

    contornos1, _ = cv2.findContours(th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos2, _ = cv2.findContours(th2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contornos1 or not contornos2:
        return 999999

    c1 = max(contornos1, key=cv2.contourArea)
    c2 = max(contornos2, key=cv2.contourArea)

    score = cv2.matchShapes(c1, c2, 1, 0.0)

    return score

# ==========================================
# CARGAR BASE
# ==========================================

base_modelos = []

for carpeta in os.listdir(CARPETA_BASE):

    ruta_carpeta = os.path.join(CARPETA_BASE, carpeta)

    if os.path.isdir(ruta_carpeta):

        for archivo in os.listdir(ruta_carpeta):

            if archivo.endswith(".png"):

                ruta_imagen = os.path.join(ruta_carpeta, archivo)

                img = cv2.imread(ruta_imagen)

                if img is not None:

                    base_modelos.append({
                        "modelo": carpeta,
                        "imagen": img
                    })

# ==========================================
# ANALIZAR RECORTES
# ==========================================

for archivo in os.listdir(CARPETA_RECORTES):

    if archivo.endswith(".png"):

        ruta = os.path.join(CARPETA_RECORTES, archivo)

        img_recorte = cv2.imread(ruta)

        mejor_modelo = "DESCONOCIDO"
        mejor_score = 999999

        for modelo_base in base_modelos:

            score = comparar_imagenes(
                img_recorte,
                modelo_base["imagen"]
            )

            if score < mejor_score:

                mejor_score = score
                mejor_modelo = modelo_base["modelo"]

        resultado = {
            "modelo": mejor_modelo,
            "score": round(float(mejor_score), 5)
        }

        print("\n====================================")
        print(f"IMAGEN: {archivo}")
        print("====================================")

        print(
            json.dumps(
                resultado,
                indent=4,
                ensure_ascii=False
            )
        )