import cv2
import numpy as np
import os

CARPETA_ENTRADA = "recortes"
CARPETA_SALIDA = "resultado_limpieza"

os.makedirs(CARPETA_SALIDA, exist_ok=True)

for archivo in os.listdir(CARPETA_ENTRADA):

    if not archivo.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    ruta = os.path.join(CARPETA_ENTRADA, archivo)

    imagen = cv2.imread(ruta)

    if imagen is None:
        continue

    # =====================================================
    # ESCALA DE GRISES
    # =====================================================

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # =====================================================
    # SUAVIZADO
    # =====================================================

    blur = cv2.GaussianBlur(gris, (5,5), 0)

    # =====================================================
    # BINARIZACIÓN
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
    # LIMPIEZA MORFOLÓGICA
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
    # ELIMINAR BORDE INFERIOR
    # =====================================================

    alto, ancho = final.shape

    final[int(alto * 0.92):alto, :] = 255

    # =====================================================
    # ELIMINAR PUNTOS PEQUEÑOS
    # =====================================================

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        255 - final,
        connectivity=8
    )

    resultado = np.ones_like(final) * 255

    for i in range(1, num_labels):

        area = stats[i, cv2.CC_STAT_AREA]

        if area > 40:

            resultado[labels == i] = 0

    final = resultado

    # =====================================================
    # GUARDAR
    # =====================================================

    salida = os.path.join(
        CARPETA_SALIDA,
        archivo
    )

    cv2.imwrite(salida, final)

    print(f"LIMPIADA: {archivo}")

print("\nFINALIZADO")