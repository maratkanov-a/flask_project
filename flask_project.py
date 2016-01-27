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
def dict(key):
    try:
        result = data[key]
    except KeyError:
        # TODO: change to abort
        result = '404'
    return result


@app.route('/dictionary', methods=['POST'])
def analog_dict():
    return 'POST'


if __name__ == '__main__':
    app.run()
