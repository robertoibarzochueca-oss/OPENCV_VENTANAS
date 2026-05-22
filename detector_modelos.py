import cv2
import numpy as np
import os
import json

CARPETA = "recortes"

# ============================================
# DETECTAR LINEAS
# ============================================

def detectar_lineas(img):

    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(
        gris,
        180,
        255,
        cv2.THRESH_BINARY_INV
    )

    lineas = cv2.HoughLinesP(
        thresh,
        1,
        np.pi / 180,
        threshold=20,
        minLineLength=15,
        maxLineGap=8
    )

    horizontales = 0
    verticales = 0

    diagonales_largas = 0

    puntos_verticales = []
    puntos_horizontales = []

    if lineas is None:
        return None

    for linea in lineas:

        x1, y1, x2, y2 = linea[0]

        dx = x2 - x1
        dy = y2 - y1

        longitud = np.sqrt(dx*dx + dy*dy)

        angulo = np.degrees(np.arctan2(dy, dx))

        # ----------------------------------------
        # HORIZONTALES
        # ----------------------------------------

        if abs(angulo) < 10:

            horizontales += 1

        # ----------------------------------------
        # VERTICALES
        # ----------------------------------------

        elif abs(angulo) > 80:

            verticales += 1

        # ----------------------------------------
        # DIAGONALES
        # ----------------------------------------

        elif 20 < abs(angulo) < 70:

            # diagonales largas = OB
            if longitud > 80:
                diagonales_largas += 1

            # diagonales pequeñas = puntas flechas
            else:

                centro_x = int((x1 + x2) / 2)
                centro_y = int((y1 + y2) / 2)

                # flechas verticales
                if abs(angulo) > 40:
                    puntos_verticales.append((centro_x, centro_y))

                # flechas horizontales
                else:
                    puntos_horizontales.append((centro_x, centro_y))

    return {
        "horizontales": horizontales,
        "verticales": verticales,
        "diagonales_largas": diagonales_largas,
        "puntos_verticales": puntos_verticales,
        "puntos_horizontales": puntos_horizontales,
        "ancho": img.shape[1]
    }

# ============================================
# DETECTOR MODELOS
# ============================================

def detectar_modelo(datos):

    diagonales = datos["diagonales_largas"]

    pv = datos["puntos_verticales"]
    ph = datos["puntos_horizontales"]

    ancho = datos["ancho"]

    # ========================================
    # OB
    # ========================================

    if diagonales >= 4:
        return "OB"

    # ========================================
    # COR
    # ========================================

    if len(ph) >= 2:
        return "COR_SIMPLE_2H_SP"

    # ========================================
    # ELV / EVO
    # ========================================

    if len(pv) >= 2:

        xs = [p[0] for p in pv]

        media_x = np.mean(xs)

        centro = ancho / 2

        # símbolo centrado = ELV
        if abs(media_x - centro) < 60:
            return "ELV_SP"

        # símbolo lateral = EVO
        else:
            return "EVOI_SP"

    return "DESCONOCIDO"

# ============================================
# RECORRER CARPETA
# ============================================

for archivo in os.listdir(CARPETA):

    if archivo.lower().endswith(".png"):

        ruta = os.path.join(CARPETA, archivo)

        img = cv2.imread(ruta)

        datos = detectar_lineas(img)

        if datos is None:
            continue

        modelo = detectar_modelo(datos)

        resultado = {
            "modelo": modelo,
            "diagonales_largas": datos["diagonales_largas"],
            "flechas_verticales": len(datos["puntos_verticales"]),
            "flechas_horizontales": len(datos["puntos_horizontales"])
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