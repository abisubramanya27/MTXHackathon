from flask import Flask,request,jsonify
from flask_cors import CORS
from PIL import Image
import pandas as pd
import os
import io
from base64 import encodebytes

def get_response_image(img):
    byte_arr = io.BytesIO()
    img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img


app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

'''Checks that the backend file structure is not damaged'''
def check_health():
    return os.path.exists('../frontend')

@app.route('/', methods=['GET', 'POST'])
def welcome():
    return ("All is Well", 200) if check_health() else ("Not Okay", 400)

@app.route('/api/submit',  methods=['POST'])
def submit():
    try:
        print(request.method, request.files)
        if request.method == 'POST':
            img = Image.open(request.files['img_file'].stream)
            annot = pd.read_json(request.files['annot_file']) if 'annot_file' in request.files else None
            encoded_img = get_response_image(img)
            output_json = annot.to_json()
            response =  { 'Status' : 'Success', 'output_json': output_json , 'output_img': encoded_img}
            return jsonify(response)
    except Exception as e:
        print(e)
        return "Error while processing submission", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
