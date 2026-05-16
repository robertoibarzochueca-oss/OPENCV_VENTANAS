import base64
import urllib.request
import json

# 1. TU LLAVE
API_KEY = "AIzaSyDWLJ4Ey8-aWmW5PtBq2qnwY_aAo27tRqU"

# 2. MONTAMOS EL MOTOR (De forma que no se pueda cortar)
base = "https://generativelanguage.googleapis.com/v1beta/models/"
modelo = "gemini-1.5-flash:generateContent"
URL = f"{base}{modelo}?key={API_KEY}"

def analizar_recorte(ruta_ventana):
    try:
        # Abrimos el recorte de OpenCV
        with open(ruta_ventana, "rb") as f:
            foto_64 = base64.b64encode(f.read()).decode("utf-8")

        # 3. LAS REGLAS DEL MAESTRO
        instrucciones = "Analiza este dibujo de ventana. Reglas: <--> es COR, Triangulo+Cruz es OB, /// es PUC. Medidas: Abajo ANCHO, derecha ALTO. Responde: MODELO | MEDIDAS | PERSIANA | EXTRAS"

        paquete = {
            "contents": [{
                "parts": [
                    {"text": instrucciones},
                    {"inline_data": {"mime_type": "image/png", "data": foto_64}}
                ]
            }]
        }

        # 4. ENVÍO DIRECTO
        req = urllib.request.Request(URL, data=json.dumps(paquete).encode("utf-8"), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            print("\n✅ ¡POR FIN! RESULTADO:")
            print(res['candidates'][0]['content']['parts'][0]['text'])
            
    except Exception as e:
        print(f"\n❌ Sigue fallando: {e}")

# Ejecutamos la prueba
analizar_recorte("ventana_1.png")