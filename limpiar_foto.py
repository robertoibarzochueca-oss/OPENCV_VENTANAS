import cv2

img = cv2.imread("foto.png")

if img is None:
    print("No existe foto.png")
    exit()

# ESCALA GRISES
gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# SUAVIZADO MUY SUAVE
limpia = cv2.GaussianBlur(gris, (3,3), 0)

# GUARDAR DIRECTAMENTE
cv2.imwrite("foto_limpia.png", limpia)

print("FOTO LIMPIA OK")