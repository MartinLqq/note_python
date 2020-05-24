from flask import Flask, request
from pathlib import Path
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/upload', methods=['POST'])
def upload():
	files = request.files.getlist('file')
	for file in files:
		print(file.filename)
		path = Path(file.filename)
		path.parent.mkdir(exist_ok=True)
		file.save(file.filename)
	return 'Uploaded success'


if __name__ == '__main__':
	app.run(debug=True, port=5000)
