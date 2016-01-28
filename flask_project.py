import json
import datetime
from os import abort
from flask import Flask, abort

app = Flask(__name__)

data = {
    'hello': 'Hello World!',
    'name': 'My name is Flask Server',
}


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/dictionary/<key>', methods=['GET'])
# @app.error_handlers(404)
def seek_and_show(key):
    if data.get(key):
        return json.dumps({key: data.get(key), "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
    else:
        abort(404)


@app.route('/dictionary/', methods=['POST'])
def add_element(request):
    params = json.loads(request.data)
    if not data.get(params.key):
        data.update({params.key: params.value})
    elif params.key and params.value:
        abort(400)
    else:
        abort(409)
    return json.dumps({params.key: params.value, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})


@app.route('/dictionary', methods=['PUT'])
def change_element(request):
    params = json.loads(request.data)
    try:
        data[params.key] = params.value
    except KeyError:
        abort(404)
    return json.dumps({params.key: params.value, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})


@app.route('/dictionary/<key>', methods=['DELETE'])
def delete_element(key):
    try:
        data.pop(key)
    except KeyError:
        pass
    return json.dumps({key: 'null', "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})


if __name__ == '__main__':
    app.run()
