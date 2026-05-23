import cv2
import numpy as np
import os

# =========================
# CARGAR IMAGEN
# =========================

img = cv2.imread("foto_limpia.png")

if img is None:
    print("NO EXISTE foto_limpia.png")
    exit()

resultado = img.copy()

alto, ancho = img.shape[:2]

# =========================
# GRISES
# =========================

gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# =========================
# BINARIZAR
# =========================

_, binaria = cv2.threshold(
    gris,
    160,
    255,
    cv2.THRESH_BINARY_INV
)

# =========================
# CONTORNOS
# =========================

contornos, _ = cv2.findContours(
    binaria,
    cv2.RETR_LIST,
    cv2.CHAIN_APPROX_SIMPLE
)

mejor = None
mejor_score = 0

# =========================
# BUSCAR MEJOR CANDIDATO
# =========================

for c in contornos:

    area = cv2.contourArea(c)

    if area < 10 or area > 400:
        continue

    x, y, w, h = cv2.boundingRect(c)

    # SOLO ARRIBA
    if y > alto * 0.30:
        continue

    # CASI CUADRADO
    ratio = w / float(h)

    if ratio < 0.7 or ratio > 1.3:
        continue

    # DENSIDAD
    roi = binaria[y:y+h, x:x+w]

    negros = cv2.countNonZero(roi)

    total = w * h

    densidad = negros / total

    # SCORE
    score = densidad * area

    if score > mejor_score:

        mejor_score = score
        mejor = (x, y, w, h)

# =========================
# DIBUJAR SOLO EL MEJOR
# =========================

if mejor is not None:

    x, y, w, h = mejor

    cv2.rectangle(
        resultado,
        (x, y),
        (x + w, y + h),
        (0, 255, 255),
        3
    )

    cv2.putText(
        resultado,
        "PERSIANA",
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2
    )

    print("")
    print("======================")
    print("PERSIANA DETECTADA")
    print("======================")
    print("")

else:

    print("")
    print("======================")
    print("NO DETECTADA")
    print("======================")
    print("")

# =========================
# GUARDAR
# =========================

os.makedirs("resultado_limpieza", exist_ok=True)

cv2.imwrite(
    "resultado_limpieza/persiana_detectada.png",
    resultado
)

print("IMAGEN GUARDADA")