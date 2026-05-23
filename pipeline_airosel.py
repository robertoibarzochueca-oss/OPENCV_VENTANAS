import os
import cv2
import numpy as np
import shutil

# =====================================================
# CONFIGURACIÓN
# =====================================================

CARPETA_RECORTES = "recortes"
CARPETA_RESULTADO = "resultado_limpieza"

# =====================================================
# LIMPIAR CARPETAS
# =====================================================

if os.path.exists(CARPETA_RECORTES):
    shutil.rmtree(CARPETA_RECORTES)

if os.path.exists(CARPETA_RESULTADO):
    shutil.rmtree(CARPETA_RESULTADO)

os.makedirs(CARPETA_RECORTES, exist_ok=True)
os.makedirs(CARPETA_RESULTADO, exist_ok=True)

# =====================================================
# CARGAR FOTO
# =====================================================

imagen = cv2.imread("foto_recibida.jpg")

if imagen is None:
    print("❌ No existe foto_recibida.jpg")
    exit()

# =====================================================
# ESCALA DE GRISES
# =====================================================

gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# =====================================================
# FILTRADO
# =====================================================

filtrada = cv2.bilateralFilter(
    gris,
    9,
    75,
    75
)

# =====================================================
# BINARIZAR
# =====================================================

binaria = cv2.adaptiveThreshold(
    filtrada,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    51,
    11
)

# =====================================================
# CERRAR TRAZOS
# =====================================================

kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (5, 5)
)

binaria = cv2.morphologyEx(
    binaria,
    cv2.MORPH_CLOSE,
    kernel
)

# =====================================================
# DILATAR UN POCO
# =====================================================

binaria = cv2.dilate(
    binaria,
    kernel,
    iterations=1
)

# =====================================================
# DETECTAR LÍNEAS
# =====================================================

alto, ancho = binaria.shape[:2]

longitud_minima = int(min(alto, ancho) * 0.10)

lineas = cv2.HoughLinesP(
    binaria,
    rho=1,
    theta=np.pi / 180,
    threshold=40,
    minLineLength=longitud_minima,
    maxLineGap=40
)

# =====================================================
# LIENZO BLANCO
# =====================================================

lienzo = np.ones_like(imagen) * 255

# =====================================================
# DIBUJAR CAPAS
# =====================================================

if lineas is not None:

    for linea in lineas:

        x1, y1, x2, y2 = linea[0]

        angulo = abs(
            np.arctan2(
                y2 - y1,
                x2 - x1
            ) * 180 / np.pi
        )

        # =================================================
        # HORIZONTALES / VERTICALES
        # =================================================

        if angulo < 15 or angulo > 165 or 75 < angulo < 105:

            color = (0, 255, 0)

            # =============================================
            # POSIBLE PERSIANA
            # =============================================

            if y1 < alto * 0.20 and y2 < alto * 0.20:
                color = (0, 255, 255)

            cv2.line(
                lienzo,
                (x1, y1),
                (x2, y2),
                color,
                3
            )

        # =================================================
        # DIAGONALES
        # =================================================

        elif 20 < angulo < 70 or 110 < angulo < 160:

            cv2.line(
                lienzo,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                3
            )

# =====================================================
# DETECTAR CONTORNOS
# =====================================================

gris_lienzo = cv2.cvtColor(
    lienzo,
    cv2.COLOR_BGR2GRAY
)

_, thresh = cv2.threshold(
    gris_lienzo,
    240,
    255,
    cv2.THRESH_BINARY_INV
)

contornos, _ = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

contador = 1

# =====================================================
# BUSCAR POSIBLES VENTANAS
# =====================================================

for c in contornos:

    area = cv2.contourArea(c)

    if area < 30000:
        continue

    x, y, w, h = cv2.boundingRect(c)

    # =================================================
    # FILTROS DE TAMAÑO
    # =================================================

    if w < 250:
        continue

    if h < 250:
        continue

    ratio = w / h

    if ratio < 0.4 or ratio > 3:
        continue

    # =================================================
    # MÁRGENES
    # =================================================

    margen = 25

    x1 = max(x - margen, 0)
    y1 = max(y - margen, 0)

    x2 = min(x + w + margen, imagen.shape[1])
    y2 = min(y + h + margen, imagen.shape[0])

    recorte_original = imagen[y1:y2, x1:x2]

    recorte_color = lienzo[y1:y2, x1:x2]

    # =================================================
    # DIBUJAR MARCO ROJO
    # =================================================

    cv2.rectangle(
        recorte_color,
        (0, 0),
        (recorte_color.shape[1]-1, recorte_color.shape[0]-1),
        (0, 0, 255),
        4
    )

    # =================================================
    # GUARDAR ORIGINAL
    # =================================================

    ruta_original = os.path.join(
        CARPETA_RECORTES,
        f"ventana_{contador}.png"
    )

    cv2.imwrite(
        ruta_original,
        recorte_original
    )

    # =================================================
    # GUARDAR COLOREADA
    # =================================================

    ruta_color = os.path.join(
        CARPETA_RESULTADO,
        f"ventana_color_{contador}.png"
    )

    cv2.imwrite(
        ruta_color,
        recorte_color
    )

    print(f"✅ Ventana detectada: {contador}")

    contador += 1

# =====================================================
# RESULTADO FINAL
# =====================================================

print(f"\nTOTAL VENTANAS: {contador - 1}")