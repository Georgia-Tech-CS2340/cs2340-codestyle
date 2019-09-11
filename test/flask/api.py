from flask import Flask
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
objects = {"ball": "red", "clown": "fun"}


class Object(Resource):
  def get(self, name):
    if name in objects.keys():
      return objects[name], 200
    else:
      return "Object {} not found".format(name), 404

  def post(self, name):
    parser = reqparse.RequestParser()
    parser.add_argument('value')
    args = parser.parse_args()
    if args.get('value') is None:
        return "Malformed request", 400
    else:
      if name not in objects.keys():
        objects[name] = args.get('value')
        return "Object {} created successfully".format(name), 201
      else:
        return "Object {} already exists".format(name), 402

  def delete(self, name):
    if name in objects.keys():
      del objects[name]
      return "Object {} deleted".format(name), 200
    else:
      return "Object {} not found".format(name), 404


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
