from flask import Flask, request, redirect, url_for, json
from flask_cors import CORS, cross_origin
import requests
from dbconnect import ChurchDB
from werkzeug.utils import secure_filename
import requests, os
import jsonify, base64

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

db = ChurchDB()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"/api/*": {"origins": "https://serene-dijkstra-1e3805.netlify.com/"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/test', methods=['GET', 'POST'])
@cross_origin()
def test():
    if request.method == 'GET':
        return json.dumps({'him': 'dance', 'other': os.path.isdir('images')})

@app.route('/api/login', methods=['GET', 'POST'])
@cross_origin()
def login():
    content = request.get_json(silent=True)
    if content['username'] == 'username' and content['password'] == 'password':
        return json.dumps({'success': True}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'success': False}), 200, {'ContentType':'application/json'}

@app.route('/api/register', methods=['GET', 'POST'])
@cross_origin()
def register():
    content = request.get_json(silent=True)
    passport_img = base64Encoder()
    content.update({'photo': passport_img })
    # next is to save the data in the database
    try:
        inserted_id = db.register('members', content)
        print('inserted ids ', inserted_id)
        if inserted_id:
            return json.dumps({'success': True}), 200, {'ContentType':'application/json'}
        else:
            return json.dumps({'success': False}), 402, {'ContentType':'application/json'}
    except Exception as e:
        print(str(e))
        return json.dumps({'success': False}), 402, {'ContentType':'application/json'}

@app.route('/api/upload', methods=['GET', 'POST'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
        if file:
            print('OKAY FILE')
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return json.dumps({'success': True}), 200, {'ContentType':'application/json'}        

@app.route('/api/uploadSuccess', methods=['GET', 'POST'])
@cross_origin()
def finished():
    if request.method == 'POST':
        return json.dumps({'success': True}), 200, {'ContentType':'application/json'}

# read image in folder and convert to base64
def base64Encoder(UPLOAD_FOLDER=UPLOAD_FOLDER):
    image_directory = os.listdir(UPLOAD_FOLDER)
    if len(os.listdir(UPLOAD_FOLDER)) > 0:
        image_path = os.listdir(UPLOAD_FOLDER)[1]
        full_path = os.path.join(UPLOAD_FOLDER, image_path)
        with open(full_path, 'rb') as imageFile:
            stringedImage = base64.b64encode(imageFile.read())
        os.remove(full_path)
        return stringedImage # store returned string to database
    else:
        return 'empty directory'

# convert base64 string back to image and save in folder
def base64Decoder(preferredFileName: str, encodedImg: str):
    UPLOAD_FOLDER = 'images'
    imageFileName = preferredFileName + '.jpg'
    full_path = os.path.join(UPLOAD_FOLDER, imgFileName)
    with open(imageFileName, 'wb') as fimage:
        fimage.write(encodedImg.decode('base64'))
    return True

if __name__=="__main__":
    app.run()
