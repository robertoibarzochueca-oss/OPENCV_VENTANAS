import cv2
import numpy as np
import os

def separar_dibujos():
    # 1. Cargar la foto original que tienes en el taller
    archivo_original = "foto.png"
    img = cv2.imread(archivo_original)
    
    if img is None:
        print(f"❌ Error: No encuentro el archivo '{archivo_original}'")
        return

    # 2. Convertir a blanco y negro para detectar los bordes
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    suave = cv2.GaussianBlur(gris, (5, 5), 0)
    _, thresh = cv2.threshold(suave, 150, 255, cv2.THRESH_BINARY_INV)

    # 3. Agrupar las líneas de cada ventana (dilatación)
    kernel = np.ones((15,15), np.uint8)
    dilatado = cv2.dilate(thresh, kernel, iterations=2)

    # 4. Encontrar los recuadros de cada dibujo
    contornos, _ = cv2.findContours(dilatado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"--- INICIANDO CORTE DE HUECOS ---")
    
    contador = 1
    for c in contornos:
        x, y, w, h = cv2.boundingRect(c)
        
        # Filtro para evitar manchas pequeñas (solo recuadros grandes)
        if w > 100 and h > 100:
            recorte = img[y:y+h, x:x+w]
            nombre = f"ventana_{contador}.png"
            cv2.imwrite(nombre, recorte)
            print(f"✅ Guardado: {nombre} ({w}x{h} píxeles)")
            contador += 1

    print(f"--- PROCESO TERMINADO: {contador-1} dibujos separados ---")

separar_dibujos()