import cv2
import numpy as np
import os
import shutil

def separar_dibujos():

    # =====================================================
    # CARPETA DE SALIDA
    # =====================================================

    CARPETA_SALIDA = "recortes"

    # =====================================================
    # BORRAR RECORTES ANTERIORES
    # =====================================================

    if os.path.exists(CARPETA_SALIDA):
        shutil.rmtree(CARPETA_SALIDA)

    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    # =====================================================
    # CARGAR FOTO NUEVA RECIBIDA
    # =====================================================

    archivo_original = "foto_recibida.jpg"

    img = cv2.imread(archivo_original)

    if img is None:
        print(f"❌ Error: No encuentro el archivo '{archivo_original}'")
        return

    # =====================================================
    # ESCALA DE GRISES
    # =====================================================

    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # =====================================================
    # SUAVIZAR
    # =====================================================

    suave = cv2.GaussianBlur(gris, (5, 5), 0)

    # =====================================================
    # BINARIZAR
    # =====================================================

    _, thresh = cv2.threshold(
        suave,
        150,
        255,
        cv2.THRESH_BINARY_INV
    )

    # =====================================================
    # AGRUPAR LÍNEAS
    # =====================================================

    kernel = np.ones((15,15), np.uint8)

    dilatado = cv2.dilate(
        thresh,
        kernel,
        iterations=2
    )

    # =====================================================
    # BUSCAR CONTORNOS
    # =====================================================

    contornos, _ = cv2.findContours(
        dilatado,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    print("\n--- INICIANDO CORTE DE HUECOS ---")

    contador = 1

    # =====================================================
    # RECORTAR CADA VENTANA
    # =====================================================

    for c in contornos:

        x, y, w, h = cv2.boundingRect(c)

        # =================================================
        # FILTRO DE TAMAÑO
        # =================================================

        if w > 100 and h > 100:

            margen = 20

            x1 = max(x - margen, 0)
            y1 = max(y - margen, 0)

            x2 = min(x + w + margen, img.shape[1])
            y2 = min(y + h + margen, img.shape[0])

            recorte = img[y1:y2, x1:x2]

            nombre = f"ventana_{contador}.png"

            ruta_salida = os.path.join(
                CARPETA_SALIDA,
                nombre
            )

            cv2.imwrite(ruta_salida, recorte)

            print(f"✅ Guardado: {nombre} ({w}x{h} píxeles)")

            contador += 1

    print(f"\n--- PROCESO TERMINADO: {contador-1} dibujos separados ---")


separar_dibujos()