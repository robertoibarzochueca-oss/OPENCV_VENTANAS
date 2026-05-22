import cv2
import os
import json
import pytesseract

# =====================================================
# CONFIGURACION TESSERACT
# =====================================================

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# =====================================================
# CARPETA RECORTES
# =====================================================

CARPETA_RECORTES = "recortes"

# =====================================================
# PALABRAS TOLERADAS PARA "FIJO"
# =====================================================

PALABRAS_FIJO = [
    "FIJO",
    "FIFO",
    "FIGO",
    "FIJD",
    "FIJC",
    "FIIO",
    "FIJ0"
]

# =====================================================
# FUNCION OCR
# =====================================================

def leer_texto(imagen):

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # ampliar imagen
    gris = cv2.resize(
        gris,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    # binarizar
    _, thresh = cv2.threshold(
        gris,
        150,
        255,
        cv2.THRESH_BINARY
    )

    # OCR
    texto = pytesseract.image_to_string(
        thresh,
        config='--psm 6'
    )

    texto = texto.upper()

    return texto

# =====================================================
# ANALISIS
# =====================================================

for archivo in os.listdir(CARPETA_RECORTES):

    if not archivo.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    ruta = os.path.join(CARPETA_RECORTES, archivo)

    imagen = cv2.imread(ruta)

    texto = leer_texto(imagen)

    fijo_detectado = False

    for palabra in PALABRAS_FIJO:

        if palabra in texto:
            fijo_detectado = True

    resultado = {
        "fijo_detectado": fijo_detectado,
        "texto_detectado": texto.strip()
    }

    print("\n====================================")
    print(f"IMAGEN: {archivo}")
    print("====================================")

    print(
        json.dumps(
            resultado,
            indent=4,
            ensure_ascii=False
        )
    )