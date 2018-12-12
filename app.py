#librerías para la app web
from flask import Flask, render_template, request, jsonify

#librerías para cargar el modelo con keras
from keras.models import model_from_json

#librerías para cargar la imagen
from PIL import Image
from io import BytesIO
from keras.preprocessing.image import img_to_array
import numpy as np

app = Flask(__name__)
model = None

def load_request_image(image):
    image = Image.open(BytesIO(image))
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize((256, 256))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image.astype('float32') / 255

    return image

def load_model():
    json_file = open('./model/model.json', 'r')
    model_json = json_file.read()
    json_file.close()
    global model
    model = model_from_json(model_json)
    model.load_weights("./model/weights.h5")

def predict_class(image_array):
    clases = ["Model 3", "Model S", "Model X"]
    y_pred = model.predict(image_array, batch_size=None, verbose=0, steps=None)
    max_score = np.argmax(y_pred, axis=1)[0]
    image_class = clases[max_score]

    return image_class

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # print(request.headers)
    image = request.files["image"].read()
    image = load_request_image(image)
    class_predicted = predict_class(image)
    image_class = { "image_class": class_predicted } 

    return jsonify(image_class)

if __name__ == "__main__":
    load_model()
    app.run(debug = False, threaded = False)