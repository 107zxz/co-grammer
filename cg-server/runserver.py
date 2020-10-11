from flask import Flask
from flask import request
from flask_cors import CORS

from build_buffer import build_python
import os

# Supress log
import logging

# CD to current directory
os.chdir("/Users/107zxz/Documents/Work/IT/CoGrammer/cg-server/")

app = Flask(__name__)
CORS(app)

# Supress useless logging
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# data = {'buffers': [
#     {'id': 0, 'name': 'Hello', 'text': '', 'lastModified': None, 'buildMessage': "", 'flagged': False}
# ]}

data = {'buffers': []}

# Not really meant to be a normal website
@app.route('/')
def warn():
    return "This is the CoGrammer dedicated server, please use the client to connect"

@app.route("/buffers", methods=['POST'])
def parse_json():
    global data
    if not request.json:
        return 'ERROR 1, NO BUFFER DATA SPECIFIED'
    else:
        print("Client", '"' + request.json['buffer']['name'] + '"', "updating buffer with data:")
        print(request.json)

        bid = request.json['buffer']['id']

        if bid > len(data['buffers']) - 1:
            print("Adding Another buffer")
            data['buffers'].append(1)

        # print(data['buffers'], bid)

        data['buffers'][bid] = request.json['buffer']

        return data

@app.route("/querybuff", methods=['POST'])
def return_buffs():
    global data
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
