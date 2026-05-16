import cv2
import numpy as np

def analizar():
    img = cv2.imread("foto_limpia.png")
    if img is None:
        print("Falta la foto limpia. Ejecuta primero limpiar_foto.py")
        return
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bordes = cv2.Canny(gris, 50, 150)
    lineas = cv2.HoughLinesP(bordes, 1, np.pi/180, 30, minLineLength=40, maxLineGap=10)
    
    diagonales = 0
    horizontales = 0
    if lineas is not None:
        for l in lineas:
            x1, y1, x2, y2 = l[0]
            angulo = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
            if 10 < angulo < 80: diagonales += 1
            elif angulo < 10 or angulo > 170: horizontales += 1

    print("\n--- RESULTADO DEL ANÁLISIS ---")
    if diagonales > 4: print("MODELO: ABA (PRACTICABLE)")
    elif horizontales > 6: print("MODELO: OBC2 (CORREDERA)")
    else: print("MODELO: No detectado claramente")
    print("------------------------------")

analizar()