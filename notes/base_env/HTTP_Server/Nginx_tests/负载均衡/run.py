import json
from flask import Flask, request
from flask_cors import CORS
from flask_script import Manager

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
manager = Manager(app)

@app.route('/')
def index():
    return "{} received a request!".format(request.host)

if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    manager.run()

# 根据此文件启动两个本地开发服务器:
"""
python run.py runserver -d -p 5001
python run.py runserver -d -p 5002
"""
