import cv2
import os

# -----------------------------
# BORRAR FOTO LIMPIA ANTERIOR
# -----------------------------
if os.path.exists("foto_limpia.png"):
    os.remove("foto_limpia.png")

# -----------------------------
# CARGAR IMAGEN
# -----------------------------
img = cv2.imread("foto_recibida.jpg")

if img is None:
    print("ERROR: no existe foto_recibida.jpg")
    exit()

# -----------------------------
# ESCALA GRISES
# -----------------------------
gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# -----------------------------
# LIMPIEZA
# -----------------------------
blur = cv2.GaussianBlur(gris, (5,5), 0)

# binario invertido
_, th = cv2.threshold(
    blur,
    180,
    255,
    cv2.THRESH_BINARY_INV
)

# -----------------------------
# GUARDAR
# -----------------------------
cv2.imwrite("foto_limpia.png", th)

print("FOTO LIMPIA GENERADA")