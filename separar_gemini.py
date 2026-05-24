import cv2
import numpy as np
import os
import shutil

# =====================================================
# CONFIGURACION MANUAL
# =====================================================

MARGEN_IZQUIERDA = 5
MARGEN_DERECHA   = 5
MARGEN_ARRIBA    = 5
MARGEN_ABAJO     = 5

# eliminar puntos menores que este tamaño
AREA_MINIMA_RUIDO = 20

# =====================================================
# LIMPIAR CARPETA DESTINO
# =====================================================

if os.path.exists("recortes_gemini"):
    shutil.rmtree("recortes_gemini")

os.makedirs("recortes_gemini")

# =====================================================
# LEER TODOS LOS RECORTES YA DETECTADOS
# =====================================================

archivos = os.listdir("recortes")

contador = 0

for archivo in archivos:

    ruta = os.path.join("recortes", archivo)

    img = cv2.imread(ruta)

    if img is None:
        continue

    # =================================================
    # RECORTAR MARGENES MANUALES
    # =================================================

    alto, ancho = img.shape[:2]

    x1 = MARGEN_IZQUIERDA
    y1 = MARGEN_ARRIBA

    x2 = ancho - MARGEN_DERECHA
    y2 = alto - MARGEN_ABAJO

    recorte = img[y1:y2, x1:x2]

    # =================================================
    # ESCALA GRISES
    # =================================================

    gris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)

    # =================================================
    # BINARIZAR
    # =================================================

    _, binaria = cv2.threshold(
        gris,
        200,
        255,
        cv2.THRESH_BINARY_INV
    )

    # =================================================
    # ELIMINAR PUNTITOS
    # =================================================

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        binaria,
        8
    )

    limpia = np.zeros_like(binaria)

    for i in range(1, num_labels):

        area = stats[i, cv2.CC_STAT_AREA]

        if area > AREA_MINIMA_RUIDO:
            limpia[labels == i] = 255

    # =================================================
    # INVERTIR
    # =================================================

    resultado = 255 - limpia

    # =================================================
    # PASAR A RGB
    # =================================================

    resultado = cv2.cvtColor(
        resultado,
        cv2.COLOR_GRAY2BGR
    )

    # =================================================
    # GUARDAR
    # =================================================

    contador += 1

    nombre = f"recortes_gemini/ventana_{contador}.png"

    cv2.imwrite(nombre, resultado)

    print(f"Gemini limpio: {contador}")

# =====================================================
# FINAL
# =====================================================

print("")
print("==========================")
print(f"TOTAL LIMPIOS: {contador}")
print("==========================")