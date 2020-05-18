import sys
import os
import cv2
import numpy as np  
from loguru import logger
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, session,request,jsonify
#from flask_wtf import FlaskForm

app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'mysecretkey'
app.config["IMAGE_UPLOADS"] = "static"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

# config logging
logger.add("file_model.log")
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")

# REMEMBER TO LOAD THE MODEL AND THE SCALER!
modelName = "modelAddDataAug200Epoc.h5"
model_malaria = load_model(modelName)


logger.info("Start with model name is {}".format(modelName))




def allowed_image(filename):
    logger.debug("Checking filename is {}".format(filename))
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    logger.debug("Checking extion file  is {}".format(ext))
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    logger.debug("Checking filesize is {}".format(filesize))
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False



# load image
def load_cv2(img_path):
    logger.debug("Path image is {}".format(img_path))
    img_data = cv2.imread(img_path)
    img_data = cv2.resize(img_data,(118,118))
    img_data = img_data/255.0
    img_data = img_data.reshape(1, 118, 118, 3)
    return img_data


@app.route("/forward", methods=["GET", "POST"])
def move_forward():
    return render_template('index.html')




@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():
  
    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            if image.filename == "":
                logger.debug("No filename and redirect to homepage")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                path_img = os.path.join(app.config["IMAGE_UPLOADS"], filename)
                image.save(path_img)
                logger.info("Save image succesful")
                new_image = load_cv2(path_img)
                # check prediction
                classes = model_malaria.predict(new_image)
                msg_result = f"Class probability :{format(classes[0][0]*100.0,'.2f')} %"
                logger.info(msg_result)
                if classes[0][0]*100.0<50:
                    results = "Cat"
                else:
                    results = "Dog"

            else:
                logger.debug("That file extension is not allowed")
                return "<h1 style='color: red;'>That file extension is not allowed!</h1>"
    
    return render_template('prediction.html',results=results,pathImage = path_img,msg = msg_result)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)