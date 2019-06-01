import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/tcm/upload/file/", methods=["POST", 'OPTIONS'])
def upload_report():
    # try:
    if len(request.files) == 0:
        return jsonify({"success": False, "message": 'select file'})
    for k in request.files:
        f = request.files[k]
        name_array = f.filename.split('.')
        dir_path = '/data/tcm/%s' % name_array[-1]
        if os.path.exists(dir_path) is False:
            os.makedirs(dir_path)
        path = os.path.join(dir_path, '.'.join(name_array[-2:]))
        f.save(path)
        return jsonify({'path': path, "message": 'success'})
    return jsonify({'len': len(request.files)})


if __name__ == '__main__':
    app.run(port=9002)
