import urllib.request
import json
import base64
import cv2

API_KEY = "AIzaSyDWLJ4Ey8-aWmW5PtBq2qnwY_aAo27tRqU"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def pedir_precio():
    try:
        # 1. Cargamos y preparamos la imagen
        img = cv2.imread("foto_limpia.png")
        if img is None:
            print("❌ No veo 'foto_limpia.png'")
            return
            
        _, buffer = cv2.imencode(".jpg", img)
        foto_64 = base64.b64encode(buffer).decode("utf-8")
        
        # 2. Estructura de datos ESTRICTA (según manual de Google)
        paquete = {
            "contents": [{
                "parts": [
                    {"text": "Analiza este dibujo de carpintería. Identifica si es ABA o OBC2 y dame presupuesto en euros. Sé breve."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": foto_64}}
                ]
            }]
        }
        
        # 3. Envío
        req = urllib.request.Request(URL, data=json.dumps(paquete).encode("utf-8"))
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as res:
            datos = json.loads(res.read().decode("utf-8"))
            print("\n🌟 ¡LO CONSEGUIMOS!:")
            print(datos['candidates'][0]['content']['parts'][0]['text'])
            
    except Exception as e:
        print(f"\n⚠️ Sigue el error: {e}")

print("--- ÚLTIMO INTENTO DEL DÍA ---")
pedir_precio()