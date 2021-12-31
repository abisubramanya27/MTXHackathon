from flask import Flask,request,Response
from PIL import Image
import pandas as pd

app = Flask(__name__)

'''Checks that the backend file structure is not damaged'''
def check_health():
    return True

@app.route('/', methods=['GET', 'POST'])
def welcome():
    return ("All is Well", 200) if check_health() else ("Not Okay", 400)


@app.route('/api/submit',  methods=['POST'])
def submit():
    try:
        if request.method == 'POST':
            img = Image.open(request.files['img_file'].stream)
            annot = pd.read_json(request.files['annot_file']) if 'annot_file' in request.files else None
            print(img.height, img.width)
            print(annot)
            return "Success", 200
    except Exception as e:
        print(e)
        return "Error while processing submission", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
