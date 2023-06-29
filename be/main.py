import os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import diem_danh
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
@cross_origin(origin='*')
def upload():
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        now = datetime.now()
        filename = secure_filename(file.filename)
        print(now.strftime("%d_%m_%Y_%H_%M_%S") + filename)
        file.save(os.path.join("./../fe/src/images", now.strftime("%d_%m_%Y_%H_%M_%S_") + filename))
        resp = jsonify({'message' : 'File successfully uploaded', "result": now.strftime("%d_%m_%Y_%H_%M_%S_") + filename})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

@app.route("/get", methods=['GET'])
@cross_origin(origin='*')
def getAllApi():
    src = request.args.get("src")
    result, src = diem_danh.diem_danh(src)
    return jsonify({"result": result, "src": src})

if __name__ == "__main__":
    app.run()