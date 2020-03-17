import os
import numpy as np  
from flask import Flask, render_template, session, redirect, url_for, session,request
from flask_wtf import FlaskForm
#from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename



app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'mysecretkey'
app.config["IMAGE_UPLOADS"] = "static"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

# REMEMBER TO LOAD THE MODEL AND THE SCALER!
catdog_model = load_model("cat_dog_detector_finetune.h5")






def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

def load_imagefrom(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_tensor = image.img_to_array(img)                    # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.                                      # imshow expects values in the range [0, 1]

    return img_tensor

@app.route("/forward", methods=["GET", "POST"])
def move_forward():
    return render_template('upload.html')

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('upload.html')


@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():
  
    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                path_img = os.path.join(app.config["IMAGE_UPLOADS"], filename)
                print(path_img)
                image.save(path_img)
                print("Image saved")
                new_image = load_imagefrom(path_img)
                # check prediction
                classes = catdog_model.predict(new_image)
                print(f"Class accuracy :{classes[0][0]*100.0} %",)
                if classes[0][0]*100.0>50:
                    results = "dog"
                else:
                    results = "cat"

            else:
                print("That file extension is not allowed")
                return "<h1 style='color: red;'>That file extension is not allowed!</h1>"
    
    return render_template('prediction.html',results=results,pathImage = path_img)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)