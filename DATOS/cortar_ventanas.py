import cv2
import numpy as np

# 1. Cargamos la foto original
imagen = cv2.imread("foto.png")

if imagen is None:
    print("❌ No encuentro 'foto.png'.")
else:
    # 2. Procesamos la imagen
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    _, binaria = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY_INV)

    # 3. Buscamos los dibujos
    contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"--- Cortando con margen generoso (150px) ---")
    
    i = 1
    for c in contornos:
        x, y, w, h = cv2.boundingRect(c)
        
        if w > 100 and h > 100:
            # MARGEN DE SEGURIDAD EXTRA (150 píxeles)
            m = 150
            y_ini, y_fin = max(0, y - m), min(imagen.shape[0], y + h + m)
            x_ini, x_fin = max(0, x - m), min(imagen.shape[1], x + w + m)

            # Cortamos la pieza
            recorte = imagen[y_ini:y_fin, x_ini:x_fin]
            cv2.imwrite(f"ventana_{i}.png", recorte)
            print(f"✅ Ventana {i} guardada con margen extra.")
            i += 1
    print(f"--- ¡Listo! Ya tienes los {i-1} recortes ---")