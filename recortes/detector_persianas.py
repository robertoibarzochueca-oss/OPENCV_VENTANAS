import cv2
import numpy as np
import os
import json

# ============================================
# CONFIGURACION
# ============================================

CARPETA = "recortes"

# ============================================
# FUNCION DETECCION PERSIANA
# ============================================

def detectar_persiana(ruta_imagen):

    imagen = cv2.imread(ruta_imagen)

    if imagen is None:
        return {
            "persiana": False,
            "manos_persiana": []
        }

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    alto, ancho = gris.shape

    # ====================================================
    # SOLO ANALIZAMOS EL 18% SUPERIOR
    # ====================================================

    zona_superior = gris[0:int(alto * 0.18), :]

    # ====================================================
    # BINARIZADO
    # ====================================================

    _, thresh = cv2.threshold(
        zona_superior,
        60,
        255,
        cv2.THRESH_BINARY_INV
    )

    # ====================================================
    # BUSCAR CONTORNOS NEGROS
    # ====================================================

    contornos, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    manos = []

    # ====================================================
    # ANALISIS CONTORNOS
    # ====================================================

    for c in contornos:

        x, y, w, h = cv2.boundingRect(c)

        area = w * h

        # ============================================
        # FILTROS BASICOS
        # ============================================

        # tamaño minimo
        if area < 20:
            continue

        # tamaño maximo
        if area > 1200:
            continue

        # evitar lineas horizontales/largas
        ratio = w / float(h)

        if ratio < 0.6 or ratio > 1.4:
            continue

        # ============================================
        # DEBE ESTAR MUY CERCA DEL BORDE
        # ============================================

        margen_lateral = int(ancho * 0.12)

        lado = None

        if x < margen_lateral:
            lado = "I"

        elif (x + w) > (ancho - margen_lateral):
            lado = "D"

        else:
            continue

        # ============================================
        # EVITAR FALSOS POSITIVOS
        # SOLO EN PARTE SUPERIOR REAL
        # ============================================

        if y > (alto * 0.08):
            continue

        # ============================================
        # COMPROBAR DENSIDAD NEGRA
        # ============================================

        roi = thresh[y:y+h, x:x+w]

        pixeles_negros = cv2.countNonZero(roi)

        densidad = pixeles_negros / float(area)

        # debe estar bastante relleno
        if densidad < 0.55:
            continue

        manos.append(lado)

    # ============================================
    # LIMPIAR DUPLICADOS
    # ============================================

    manos = list(set(manos))

    # ============================================
    # RESULTADO FINAL
    # ============================================

    return {
        "persiana": len(manos) > 0,
        "manos_persiana": manos
    }

# ============================================
# RECORRER IMAGENES
# ============================================

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