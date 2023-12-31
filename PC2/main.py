import tempfile
import os
from flask import Flask, request, redirect, send_file, render_template, jsonify
from tensorflow.keras.models import load_model
from skimage import io
import base64
import glob
import numpy as np
import cv2




value = None
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # check if the post request has the file part
        img_data = request.form.get('myImage').replace("data:image/png;base64,","")
        aleatorio = request.form.get('numero')
        print(aleatorio)
        with tempfile.NamedTemporaryFile(delete = False, mode = "w+b", suffix='.png', dir=str(aleatorio)) as fh:
            fh.write(base64.b64decode(img_data))
        #file = request.files['myImage']
        print("Image uploaded")
    except Exception as err:
        print("Error occurred")
        print(err)

    return redirect("/", code=302)


@app.route('/prepare', methods=['GET'])
def prepare_dataset():
    images = []
    d = ["owo", "unu", "uwu","7u7"]
    digits = []
    print("prueba")
    for digit in d:
      print("mm")
      filelist = glob.glob('{}/*.png'.format(digit))
      images_read = io.concatenate_images(io.imread_collection(filelist))
      images_read = images_read[:, :, :, 3]
      digits_read = np.array([d.index(digit)] * images_read.shape[0], dtype=np.int32)
      images.append(images_read)
      digits.append(digits_read)
    print("fuera del for")
    images = np.vstack(images)
    digits = np.concatenate(digits)
    np.save('X.npy', images)
    np.save('y.npy', digits)
    print("final")
    return "OK!"

@app.route('/X.npy', methods=['GET'])
def download_X():
    return send_file('./X.npy')
@app.route('/y.npy', methods=['GET'])
def download_y():
    return send_file('./y.npy')


@app.route('/predict')
def predict_page():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # check if the post request has the file part
        img_data = request.form.get('myImage').replace("data:image/png;base64,","")
        valor = 4
        print("Image charged")
        return render_template('predict.html',value=valor)  
            
    except Exception as err:
        print("Error occurred")
        print(err)

   
        
if __name__ == "__main__":
    digits = ["owo", "unu", "uwu","7u7"]
    for d in digits:
        if not os.path.exists(str(d)):
            os.mkdir(str(d))
    app.run()
