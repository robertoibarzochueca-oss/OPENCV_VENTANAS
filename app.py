from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/procesar", methods=["POST"])
def procesar():

    foto = request.form.get("foto")

    return jsonify({
        "ok": True,
        "foto_recibida": foto
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)