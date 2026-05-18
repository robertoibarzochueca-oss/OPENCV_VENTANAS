import cv2
import os

# =========================
# CREAR CARPETA RECORTES
# =========================

os.makedirs("recortes", exist_ok=True)

# BORRAR RECORTES ANTERIORES
for archivo in os.listdir("recortes"):

    ruta = os.path.join("recortes", archivo)

    if os.path.isfile(ruta):
        os.remove(ruta)

# =========================
# LEER IMAGENES
# =========================

img = cv2.imread("foto_limpia.png")

if img is None:
    print("No existe foto_limpia.png")
    exit()

# FOTO ORIGINAL
original = cv2.imread("foto.png")

# =========================
# DETECCION BORDES
# =========================

gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

bordes = cv2.Canny(
    gris,
    70,
    170
)

# =========================
# CONTORNOS
# =========================

contornos, _ = cv2.findContours(
    bordes,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

contador = 1

alto_img, ancho_img = original.shape[:2]

for c in contornos:

    area = cv2.contourArea(c)

    # FILTRAR BASURA
    if area < 15000:
        continue

    x, y, w, h = cv2.boundingRect(c)

    # FILTRAR COSAS PEQUEÑAS
    if w < 120 or h < 120:
        continue

    # EVITAR FOTO ENTERA
    if w > ancho_img * 0.80:
        continue

    if h > alto_img * 0.80:
        continue

    # =========================
    # MARGENES
    # =========================

    margen_x = 90
    margen_y = 110

    # EXTRA ABAJO
    extra_abajo = 80

    x1 = max(x - margen_x, 0)
    y1 = max(y - margen_y, 0)

    x2 = min(x + w + margen_x, ancho_img)
    y2 = min(y + h + margen_y + extra_abajo, alto_img)

    recorte = original[y1:y2, x1:x2]

    nombre = f"recortes/ventana_{contador}.png"

    cv2.imwrite(nombre, recorte)

    print(f"Guardado: {nombre}")

    contador += 1

# =========================
# FINAL
# =========================

print("----------------------")
print("PROCESO TERMINADO")
print("----------------------")