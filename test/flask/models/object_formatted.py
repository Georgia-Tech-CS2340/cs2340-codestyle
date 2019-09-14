from flask_restful import Resource, reqparse

objects = {"ball": "red", "clown": "fun"}


def format_message(name, message):
    return "Object {} {}".format(name, message)


class Object(Resource):
    def get(name):
        if name in objects.keys():
            return objects[name], 200
        return format_message(name, "not found"), 404

    def post(name):
        parser = reqparse.RequestParser()
        parser.add_argument('value')
        args = parser.parse_args()
        if args.get('value') is None:
            return "Malformed request", 400
        else:
            if name not in objects.keys():
                objects[name] = args.get('value')
                return format_message(name, "created successfully").format(name), 201
            else:
                return "Object {} already exists".format(name), 402

    def delete(name):
        if name in objects.keys():
            del objects[name]
            return "Object {} deleted".format(name), 200
        else:
            return format_message(name, "not found"), 404
