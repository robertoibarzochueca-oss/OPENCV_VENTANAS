import cv2
import numpy as np
import os
import json

CARPETA = "recortes"

def detectar_persiana(ruta):

    img = cv2.imread(ruta)

    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    alto, ancho = gris.shape

    # =====================================================
    # BINARIZADO
    # =====================================================

    _, th = cv2.threshold(
        gris,
        170,
        255,
        cv2.THRESH_BINARY_INV
    )

    # =====================================================
    # SOLO FRANJA SUPERIOR
    # =====================================================

    zona_superior = th[0:int(alto * 0.15), :]

    contornos, _ = cv2.findContours(
        zona_superior,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    manos = []

    for c in contornos:

        x, y, w, h = cv2.boundingRect(c)

        area = w * h

        # =====================================================
        # FILTROS
        # =====================================================

        # pequeños cuadrados
        if area < 5 or area > 300:
            continue

        # forma cuadrada
        ratio = w / float(h)

        if ratio < 0.5 or ratio > 1.5:
            continue

        # =====================================================
        # SOLO LATERALES
        # =====================================================

        if x < ancho * 0.12:

            manos.append("I")

        elif (x + w) > ancho * 0.88:

            manos.append("D")

    manos = list(set(manos))

    return {
        "persiana": len(manos) > 0,
        "manos_persiana": manos
    }

# =====================================================
# RECORRER IMAGENES
# =====================================================

for archivo in os.listdir(CARPETA):

    if archivo.lower().endswith((".png", ".jpg", ".jpeg")):

        ruta = os.path.join(CARPETA, archivo)

        resultado = detectar_persiana(ruta)

        print("\n====================================")
        print(f"IMAGEN: {archivo}")
        print("====================================")

        print(json.dumps(
            resultado,
            indent=4,
            ensure_ascii=False
        ))