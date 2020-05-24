import json
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/vod/')
def vod_index():
    return "Hello vod"

@app.route('/vod/bar')
def vod_bar():
    return "Bar!"

if __name__ == '__main__':
    app.run(debug=True, port=8002)
