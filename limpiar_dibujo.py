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
    # ENGORDAR
    # =====================================================

    limpio = cv2.dilate(
        limpio,
        kernel,
        iterations=1
    )

    # =====================================================
    # COMPONENTES
    # =====================================================

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        limpio,
        connectivity=8
    )

    alto_total, ancho_total = limpio.shape

    mejor_area = 0
    mejor_x = 0
    mejor_y = 0
    mejor_w = ancho_total
    mejor_h = alto_total

    # =====================================================
    # BUSCAR EL DIBUJO PRINCIPAL
    # =====================================================

    for i in range(1, num_labels):

        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]

        if area < 250:
            continue

        if w < ancho_total * 0.35:
            continue

        if h < alto_total * 0.35:
            continue

        if area > mejor_area:

            mejor_area = area

            mejor_x = x
            mejor_y = y
            mejor_w = w
            mejor_h = h

    # =====================================================
    # MÁRGENES MÁS AMPLIOS
    # =====================================================

    margen_lateral =  70
    margen_superior = 65
    margen_inferior = 55

    x1 = max(mejor_x - margen_lateral, 0)
    y1 = max(mejor_y - margen_superior, 0)

    x2 = min(mejor_x + mejor_w + margen_lateral, ancho_total)
    y2 = min(mejor_y + mejor_h + margen_inferior, alto_total)

    recorte = limpio[y1:y2, x1:x2]

    # =====================================================
    # ELIMINAR RESTOS ARRIBA
    # =====================================================

    alto_recorte = recorte.shape[0]

    banda_superior = int(alto_recorte * 0.08)

    recorte[0:banda_superior, :] = cv2.medianBlur(
        recorte[0:banda_superior, :],
        9
    )

    # =====================================================
    # INVERTIR
    # =====================================================

    final = 255 - recorte

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