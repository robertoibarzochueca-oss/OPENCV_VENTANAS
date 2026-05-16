import cv2
import numpy as np
import os

def limpiar():
    archivo = "foto.png" # Asegúrate de que tu dibujo se llame así
    img = cv2.imread(archivo)
    if img is None:
        print(f"No encuentro {archivo}")
        return
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    suave = cv2.GaussianBlur(gris, (5, 5), 0)
    _, bn = cv2.threshold(suave, 150, 255, cv2.THRESH_BINARY_INV)
    final = cv2.bitwise_not(bn)
    cv2.imwrite("foto_limpia.png", final)
    print("✨ PASO 1 COMPLETADO: Foto limpia creada como 'foto_limpia.png'")

limpiar()