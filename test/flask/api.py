from flask import Flask
from flask_restful import Api
from models.object import Object


app = Flask(__name__)


@app.route('/')
def base():
    return "hello world"


@app.route('/versions/<number>')
def version_string(number):
    return "running on version {}".format(number)


@app.route('/status', methods=['GET'])
def status():
    return "all systems operational", 204


def app_factory():
    api = Api(app)
    api.add_resource(Object, "/object/<string:name>")
    return app
