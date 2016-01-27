import json
from flask import Flask

app = Flask(__name__)

data = {
    'hello': 'Hello World!',
    'name': 'My name is Flask Server',
}

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/dictionary/<key>', methods=['GET'])
def seek_and_show(key):
    try:
        result = data[key]
    except KeyError:
        result = '404'
    return data


@app.route('/dictionary/', methods=['POST'])
def add_element(request):
    params = json.loads(request.data)
    if not data.get(params.key):
        data.update({params.key: params.value})
        code = '200'
    elif params.key and params.value:
        code = 400
    else:
        code = 409
    return code


@app.route('/dictionary', methods=['PUT'])
def change_element(request):
    params = json.loads(request.data)
    try:
        data[request.key] = request.value
        code = '200'
    except KeyError:
        code = '404'
    return code


@app.route('/dictionary/<key>', methods=['DELETE'])
def delete_element(key):
    try:
        data.pop(key)
    except KeyError:
        pass
    return '200'


if __name__ == '__main__':
    app.run()
