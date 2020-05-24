import json
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/edu')
def edu_index():
    return "Hello edu"

@app.route('/edu/foo')
def edu_foo():
    return "Foo!"

if __name__ == '__main__':
    app.run(debug=True, port=8001)
