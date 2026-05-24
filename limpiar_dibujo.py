import cv2
import numpy as np
import os

# ==========================================
# CARGAR FOTO
# ==========================================

img = cv2.imread("foto_recibida.png")

if img is None:
    print("ERROR: no existe foto_recibida.png")
    exit()

# ==========================================
# ESCALA GRISES
# ==========================================

gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ==========================================
# SUAVIZAR
# ==========================================

blur = cv2.GaussianBlur(gris, (5,5), 0)

# ==========================================
# THRESHOLD ADAPTATIVO
# ==========================================

binaria = cv2.adaptiveThreshold(
    blur,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    21,
    8
)

# ==========================================
# LIMPIAR RUIDO
# ==========================================

kernel = np.ones((3,3), np.uint8)

limpia = cv2.morphologyEx(
    binaria,
    cv2.MORPH_OPEN,
    kernel
)

# ==========================================
# ENGORDAR LINEAS
# ==========================================

limpia = cv2.dilate(
    limpia,
    kernel,
    iterations=1
)

# ==========================================
# INVERTIR
# ==========================================

final = 255 - limpia

# ==========================================
# GUARDAR
# ==========================================

cv2.imwrite("foto_limpia.png", final)

print("FOTO LIMPIA GENERADA")