import cv2
import numpy as np
import os
import shutil

# ==========================================
# BORRAR RECORTES ANTERIORES
# ==========================================

if os.path.exists("recortes"):
    shutil.rmtree("recortes")

os.makedirs("recortes")

# ==========================================
# CARGAR IMAGEN
# ==========================================

img = cv2.imread("foto_limpia.png")

if img is None:
    print("ERROR: no existe foto_limpia.png")
    exit()

gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ==========================================
# INVERTIR
# ==========================================

invertida = 255 - gris

# ==========================================
# THRESHOLD
# ==========================================

_, binaria = cv2.threshold(
    invertida,
    40,
    255,
    cv2.THRESH_BINARY
)

# ==========================================
# DILATAR
# ==========================================

kernel = np.ones((5,5), np.uint8)

dilatada = cv2.dilate(
    binaria,
    kernel,
    iterations=2
)

# ==========================================
# CONTORNOS EXTERNOS SOLO
# ==========================================

contornos, _ = cv2.findContours(
    dilatada,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

# ==========================================
# RECTANGULOS VALIDOS
# ==========================================

rectangulos = []

for c in contornos:

    x, y, w, h = cv2.boundingRect(c)

    area = w * h

    if area < 40000:
        continue

    # ignorar mancha negra izquierda
    if x < 100 and h > img.shape[0] * 0.5:
        continue

    rectangulos.append((x, y, w, h))

# ==========================================
# ELIMINAR RECTANGULOS DENTRO DE OTROS
# ==========================================

finales = []

for i, (x1, y1, w1, h1) in enumerate(rectangulos):

    dentro = False

    for j, (x2, y2, w2, h2) in enumerate(rectangulos):

        if i == j:
            continue

        if (
            x1 > x2 and
            y1 > y2 and
            x1 + w1 < x2 + w2 and
            y1 + h1 < y2 + h2
        ):
            dentro = True
            break

    if not dentro:
        finales.append((x1, y1, w1, h1))

# ==========================================
# ORDENAR
# ==========================================

finales = sorted(finales, key=lambda r: (r[1], r[0]))

# ==========================================
# GUARDAR
# ==========================================

contador = 0

for x, y, w, h in finales:

    margen = 130

    x1 = max(x - margen, 0)
    y1 = max(y - margen, 0)

    x2 = min(x + w + margen, img.shape[1])
    y2 = min(y + h + margen, img.shape[0])

    recorte = img[y1:y2, x1:x2]

    contador += 1

    nombre = f"recortes/ventana_{contador}.png"

    cv2.imwrite(nombre, recorte)

    print(f"Ventana detectada: {contador}")

# ==========================================
# FINAL
# ==========================================

print("")
print("===================")
print("TOTAL:", contador)
print("===================")