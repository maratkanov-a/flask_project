import json
import datetime
from os import abort
from flask import Flask, abort, render_template, request

app = Flask(__name__)

# main dict
data = {}


@app.route('/')
def hello_world():
    return 'Hello World!'



@app.errorhandler(404)
def page_not_found(error):
    return json.dumps({'code': 404, 'message': 'Sorry, not this URL'}), 404


@app.errorhandler(400)
def page_not_found(error):
    return json.dumps({'code': 400, 'message': 'Bad request'}), 400


@app.errorhandler(409)
def page_not_found(error):
    return json.dumps({'code': 409, 'message': 'We have conflict'}), 409


@app.route('/dictionary/<key>', methods=['GET'])
def seek_and_show(key):
    if data.get(key):
        return json.dumps({key: data.get(key), "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
    else:
        abort(404)


@app.route('/dictionary', methods=['POST'])
def add_element():
    params = json.loads(request.data)
    # check params
    if not params['key'] or not params['value']:
        abort(400)
    # check element existence
    elif not data.get(params['key']):
        data.update({params['key']: params['value']})
    # if same element alert
    else:
        abort(409)
    return json.dumps({params['key']: params['value'], "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})


@app.route('/dictionary', methods=['PUT'])
def change_element():
    params = json.loads(request.data)
    if data.get(params['key']):
        data[params['key']] = params['value']
    else:
        abort(404)
    return json.dumps({params['key']: params['value'], "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})


@app.route('/dictionary/<key>', methods=['DELETE'])
def delete_element(key):
    try:
        data.pop(key)
    except KeyError:
        pass
    return json.dumps({key: 'null', "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})


if __name__ == '__main__':
    app.run()
