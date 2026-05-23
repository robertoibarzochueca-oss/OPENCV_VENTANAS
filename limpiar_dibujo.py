import cv2
import numpy as np

# =====================================================
# CARGAR FOTO NUEVA RECIBIDA DESDE TALLY
# =====================================================

imagen = cv2.imread("foto_recibida.jpg")

if imagen is None:
    print("ERROR: no existe foto_recibida.jpg")
    exit()

# =====================================================
# GRISES
# =====================================================

gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# =====================================================
# SUAVIZADO
# =====================================================

blur = cv2.GaussianBlur(gris, (5,5), 0)

# =====================================================
# BINARIZAR
# =====================================================

binaria = cv2.adaptiveThreshold(
    blur,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    31,
    12
)

# =====================================================
# LIMPIEZA
# =====================================================

kernel = np.ones((2,2), np.uint8)

limpio = cv2.morphologyEx(
    binaria,
    cv2.MORPH_OPEN,
    kernel
)

# =====================================================
# ENGORDAR LÍNEAS
# =====================================================

limpio = cv2.dilate(
    limpio,
    kernel,
    iterations=1
)

# =====================================================
# INVERTIR
# =====================================================

final = 255 - limpio

# =====================================================
# GUARDAR FOTO LIMPIA
# =====================================================

cv2.imwrite("foto_limpia.png", final)

print("FOTO LIMPIADA")