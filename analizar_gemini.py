from google import genai
from PIL import Image
import os

# =========================================
# API KEY
# =========================================

cliente = genai.Client(
    api_key="AIzaSyA5TdXMVyDUD3DNiFCeOTQeKKm_IGs86_0"
)

# =========================================
# CARPETA RECORTES
# =========================================

CARPETA = "recortes"

# =========================================
# RECORRER IMAGENES
# =========================================

for archivo in os.listdir(CARPETA):

    if archivo.endswith(".png"):

        ruta = os.path.join(CARPETA, archivo)

        print("\n==============================")
        print("ANALIZANDO:", archivo)
        print("==============================")

        imagen = Image.open(ruta)

        prompt = """
Analiza este croquis de ventana.

Devuelve:
- tipo de ventana
- medidas visibles
- si tiene persiana
- si tiene fijo
- tipo de apertura

NO expliques nada.
"""

        respuesta = cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, imagen]
        )

        print("\nRESULTADO:")
        print(respuesta.text)

print("\n==============================")
print("FINALIZADO")
print("==============================")