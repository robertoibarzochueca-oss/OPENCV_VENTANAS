import cv2
import numpy as np

def analizar_dibujo_tecnico(ruta):
    # 1. Cargar la imagen limpia
    img = cv2.imread(ruta)
    if img is None:
        print("No encuentro la imagen limpia.")
        return
    
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Detectar líneas (Hough Transform)
    # Esto busca líneas rectas en el dibujo
    bordes = cv2.Canny(gris, 50, 150)
    lineas = cv2.HoughLinesP(bordes, 1, np.pi/180, threshold=30, minLineLength=40, maxLineGap=10)

    print(f"\n--- RESULTADO DEL ANÁLISIS TÉCNICO ---")
    
    modelo_detectado = "DESCONOCIDO"
    detalles = []

    if lineas is not None:
        diagonales = 0
        horizontales = 0
        
        for l in lineas:
            x1, y1, x2, y2 = l[0]
            # Calculamos la inclinación de la línea
            angulo = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
            
            if 10 < angulo < 80: # Si la línea está inclinada (un triángulo)
                diagonales += 1
            elif angulo < 10 or angulo > 170: # Si es plana (una flecha de corredera)
                horizontales += 1

        # 3. LÓGICA DE CARPINTERO
        if diagonales > 4:
            modelo_detectado = "ABA (PRACTICABLE)"
            detalles.append("- Detectados picos de apertura (triángulos).")
        elif horizontales > 6:
            modelo_detectado = "OBC2 (CORREDERA)"
            detalles.append("- Detectadas guías o flechas horizontales.")
            
    # 4. Mostrar resultado
    print(f"MODELO IDENTIFICADO: {modelo_detectado}")
    for d in detalles:
        print(d)
    print("--------------------------------------")

# Ejecutamos sobre la foto que limpiamos antes
analizar_dibujo_tecnico("foto_limpia.png")