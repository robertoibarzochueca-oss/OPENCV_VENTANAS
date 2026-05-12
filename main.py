import cv2
import numpy as np
import os

# 1. Cargar imagen
imagen = cv2.imread('image.png')
if imagen is None:
    print("Error: Revisa el nombre del archivo 'image.png'")
    exit()

# 2. Procesado de imagen
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
difuminado = cv2.GaussianBlur(gris, (5, 5), 0)
umbral = cv2.adaptiveThreshold(difuminado, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 4)

# Engrosar líneas
kernel = np.ones((5,5), np.uint8)
dilatado = cv2.dilate(umbral, kernel, iterations=1)

# 3. Buscar contornos
contornos, _ = cv2.findContours(dilatado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if not os.path.exists('recortes'):
    os.makedirs('recortes')

# Ordenar de arriba a abajo
contornos = sorted(contornos, key=lambda c: cv2.boundingRect(c)[1])

i = 0
for c in contornos:
    x, y, w, h = cv2.boundingRect(c)
    
    # Filtro de tamaño para ventanas reales
    if w > 150 and h > 150 and w < imagen.shape[1]*0.9:
        
        # --- MARGEN EXTRA AMPLIO (120 px) ---
        margen = 120 
        y1 = max(0, y - margen)
        y2 = min(imagen.shape[0], y + h + margen)
        x1 = max(0, x - margen)
        x2 = min(imagen.shape[1], x + w + margen)
        
        recorte = imagen[y1:y2, x1:x2]
        cv2.imwrite(f'recortes/ventana_{i}.png', recorte)
        print(f"-> RECORTADO: Ventana {i} con margen de seguridad amplio.")
        i += 1

print(f"\nANÁLISIS TOTAL: {i} ventanas listas para revisión.")