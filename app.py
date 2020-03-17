import os
import cv2
import numpy as np  
from flask import Flask, render_template, session, redirect, url_for, session,request,jsonify
from flask_wtf import FlaskForm
#from PIL import Image
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename




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



def load_cv2(img_path):
    img_data = cv2.imread(img_path)
    img_data = cv2.resize(img_data,(128,128))
    img_data = img_data/255.0
    img_data = img_data.reshape(1, 128, 128, 3)
    return img_data

app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'mysecretkey'
app.config["IMAGE_UPLOADS"] = "static"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

# REMEMBER TO LOAD THE MODEL AND THE SCALER!
catdog_model = load_model("cat_dog_detector_finetune.h5")



@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"



'''

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
                new_image = load_cv2(path_img)
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
'''

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run()