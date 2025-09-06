from flask import Flask, request, jsonify, render_template
import base64
import io
from PIL import Image
import numpy as np
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app)

# Simulated prediction pipeline class
class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename

    def predict(self):
        # For demo: simple dummy prediction based on image size or random
        try:
            img = Image.open(self.filename)
            width, height = img.size
            # Dummy logic: if width > height label as Tumor else Normal
            if width > height:
                return ["Tumor"]
            else:
                return ["Normal"]
        except Exception as e:
            print("Error in predict:", e)
            return ["Prediction failed"]

# Simple base64 decode function
def decodeImage(base64_string, filename):
    try:
        with open(filename, "wb") as f:
            f.write(base64.b64decode(base64_string))
    except Exception as e:
        print("Error decoding image:", e)
        raise

# Create global ClientApp instance for reuse
class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline(self.filename)

clApp = ClientApp()

@app.route("/", methods=["GET"])
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
@cross_origin()
def predictRoute():
    try:
        image_base64 = request.json["image"]
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]
        decodeImage(image_base64, clApp.filename)
        result = clApp.classifier.predict()
        return jsonify(result)
    except Exception as e:
        print("Prediction error:", e)
        return jsonify({"result": "Prediction failed."}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))   # Render assigns the port
    app.run(host="0.0.0.0", port=port, debug=False)  # Production-safe
