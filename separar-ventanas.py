import cv2
import os
import shutil

# -----------------------------------
# BORRAR RECORTES ANTERIORES
# -----------------------------------
if os.path.exists("recortes"):
    shutil.rmtree("recortes")

os.makedirs("recortes")

# -----------------------------------
# CARGAR FOTO LIMPIA
# -----------------------------------
img = cv2.imread("foto_limpia.png")

if img is None:
    print("ERROR: no existe foto_limpia.png")
    exit()

gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# -----------------------------------
# CONTORNOS
# -----------------------------------
contornos, _ = cv2.findContours(
    gris,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

contador = 0

# -----------------------------------
# RECORRER CONTORNOS
# -----------------------------------
for c in contornos:

    x, y, w, h = cv2.boundingRect(c)

    area = w * h

    # FILTRO TAMAÑO
    if area < 100000:
        continue

    # FILTRO DIMENSIONES
    if w < 200 or h < 200:
        continue

    contador += 1

    recorte = img[y:y+h, x:x+w]

    nombre = f"recortes/ventana_{contador}.png"

    cv2.imwrite(nombre, recorte)

    print(f"Ventana detectada: {contador}")

# -----------------------------------
# RESULTADO FINAL
# -----------------------------------
print("-----------------------")
print(f"TOTAL VENTANAS: {contador}")
print("-----------------------")