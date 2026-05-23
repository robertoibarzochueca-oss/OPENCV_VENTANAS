from flask import Flask, request, jsonify
import requests
import os
import shutil

app = Flask(__name__)

@app.route("/procesar", methods=["POST"])
def procesar():

    # =====================================================
    # BORRAR RECORTES ANTIGUOS
    # =====================================================

    carpeta_recortes = "recortes"
    carpeta_limpieza = "resultado_limpieza"

    if os.path.exists(carpeta_recortes):
        shutil.rmtree(carpeta_recortes)

    if os.path.exists(carpeta_limpieza):
        shutil.rmtree(carpeta_limpieza)

    os.makedirs(carpeta_recortes, exist_ok=True)
    os.makedirs(carpeta_limpieza, exist_ok=True)

    # =====================================================
    # RECIBIR FOTO
    # =====================================================

    url_foto = request.form.get("foto")

    response = requests.get(url_foto)

    with open("foto_recibida.jpg", "wb") as f:
        f.write(response.content)

    print("FOTO RECIBIDA")

    # =====================================================
    # EJECUTAR SCRIPTS
    # =====================================================

    os.system("py separar-ventanas.py")

    os.system("py limpiar_dibujo.py")

    print("PROCESO TERMINADO")

    # =====================================================
    # RESPUESTA
    # =====================================================

    return jsonify({
        "ok": True
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)