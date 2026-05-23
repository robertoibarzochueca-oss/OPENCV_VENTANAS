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
# NORMALIZAR ILUMINACIÓN
# =====================================================

gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

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
    (3, 3)
)

binaria = cv2.morphologyEx(
    binaria,
    cv2.MORPH_CLOSE,
    kernel
)

# =====================================================
# DETECTAR LÍNEAS
# =====================================================

alto, ancho = binaria.shape[:2]

longitud_minima = int(min(alto, ancho) * 0.12)

lineas = cv2.HoughLinesP(
    binaria,
    rho=1,
    theta=np.pi / 180,
    threshold=50,
    minLineLength=longitud_minima,
    maxLineGap=20
)

# =====================================================
# LIENZO LIMPIO
# =====================================================

lienzo = np.ones_like(imagen) * 255

# =====================================================
# DIBUJAR GEOMETRÍA
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

        # =============================================
        # HORIZONTALES / VERTICALES
        # =============================================

        if angulo < 15 or angulo > 165 or 75 < angulo < 105:

            color = (0, 255, 0)

            # =========================================
            # POSIBLE PERSIANA
            # =========================================

            if y1 < alto * 0.18 and y2 < alto * 0.18:
                color = (0, 255, 255)

            cv2.line(
                lienzo,
                (x1, y1),
                (x2, y2),
                color,
                3
            )

        # =============================================
        # DIAGONALES
        # =============================================

        elif 20 < angulo < 70 or 110 < angulo < 160:

            cv2.line(
                lienzo,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                3
            )

# =====================================================
# DETECTAR CONTORNOS GRANDES
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
# RECORTAR VENTANAS
# =====================================================

for c in contornos:

    area = cv2.contourArea(c)

    if area < 50000:
        continue

    perimetro = cv2.arcLength(c, True)

    approx = cv2.approxPolyDP(
        c,
        0.02 * perimetro,
        True
    )

    if len(approx) != 4:
        continue

    x, y, w, h = cv2.boundingRect(approx)

    if w < 300 or h < 300:
        continue

    margen = 20

    x1 = max(x - margen, 0)
    y1 = max(y - margen, 0)

    x2 = min(x + w + margen, imagen.shape[1])
    y2 = min(y + h + margen, imagen.shape[0])

    recorte_original = imagen[y1:y2, x1:x2]

    recorte_color = lienzo[y1:y2, x1:x2]

    # =============================================
    # GUARDAR ORIGINAL
    # =============================================

    nombre_original = os.path.join(
        CARPETA_RECORTES,
        f"ventana_{contador}.png"
    )

    cv2.imwrite(
        nombre_original,
        recorte_original
    )

    # =============================================
    # GUARDAR COLOREADA
    # =============================================

    nombre_color = os.path.join(
        CARPETA_RESULTADO,
        f"ventana_color_{contador}.png"
    )

    cv2.imwrite(
        nombre_color,
        recorte_color
    )

    print(f"✅ Ventana {contador}")

    contador += 1

print(f"\nTOTAL VENTANAS: {contador - 1}")