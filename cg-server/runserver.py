from flask import Flask
from flask import request
from flask_cors import CORS

from build_buffer import build_python

# Supress log
import logging

app = Flask(__name__)
CORS(app)

# Supress useless logging
logging.getLogger('werkzeug').setLevel(logging.ERROR)

data = {'buffers': [
    {'id': 0, 'text': '', 'lastModified': None, 'buildMessage': ""}, 
    {'id': 1, 'text': '', 'lastModified': None, 'buildMessage': ""},  
    {'id': 2, 'text': '', 'lastModified': None, 'buildMessage': ""}
]}

# Not really meant to be a normal website
@app.route('/')
def warn():
    return "This is the CoGrammer dedicated server, please use the client to connect"

@app.route("/buffers", methods=['POST'])
def parse_json():
    global data
    if not request.json:
        return data
    else:
        bid = request.json['buffer']['id']
        data['buffers'][bid] = request.json['buffer']

        return data

@app.route("/build", methods=['POST'])
def build():
    global data

    bid = request.json['buffer']['id']

    msg = build_python(data['buffers'][bid]['text'])

    data['buffers'][bid]['buildMessage'] = msg

    return data


if __name__ == '__main__':
    app.run()
