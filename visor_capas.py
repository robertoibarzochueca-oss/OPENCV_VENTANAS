import cv2
import numpy as np
import os

# =========================
# CARGAR IMAGEN
# =========================

img = cv2.imread("foto_recibida.jpg")

if img is None:
    print("No encuentro foto_recibida.jpg")
    exit()

original = img.copy()

# =========================
# LIMPIAR
# =========================

gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gris, (5,5), 0)

_, thresh = cv2.threshold(
    blur,
    170,
    255,
    cv2.THRESH_BINARY_INV
)

# =========================
# DETECTAR LINEAS
# =========================

lineas = cv2.HoughLinesP(
    thresh,
    1,
    np.pi / 180,
    threshold=40,
    minLineLength=80,
    maxLineGap=20
)

# =========================
# CAPAS
# =========================

resultado = np.ones_like(img) * 255

if lineas is not None:

    for linea in lineas:

        x1, y1, x2, y2 = linea[0]

        dx = x2 - x1
        dy = y2 - y1

        angulo = abs(np.degrees(np.arctan2(dy, dx)))

        # =====================
        # HORIZONTALES = VERDE
        # =====================

        if angulo < 10:

            color = (0,255,0)

        # =====================
        # VERTICALES = AZUL
        # =====================

        elif angulo > 80:

            color = (255,0,0)

        # =====================
        # DIAGONALES = ROJO
        # =====================

        else:

            color = (0,0,255)

        cv2.line(
            resultado,
            (x1,y1),
            (x2,y2),
            color,
            3
        )

# =========================
# DETECTAR CUADRADOS
# =========================

contornos, _ = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

for c in contornos:

    area = cv2.contourArea(c)

    if area < 20:
        continue

    x, y, w, h = cv2.boundingRect(c)

    ratio = w / float(h)

    # cuadrado aproximado
    if 0.7 < ratio < 1.4 and w < 120 and h < 120:

        cv2.rectangle(
            resultado,
            (x,y),
            (x+w,y+h),
            (0,255,255),
            3
        )

# =========================
# GUARDAR
# =========================

cv2.imwrite("visor_capas.png", resultado)

print("VISOR GENERADO")