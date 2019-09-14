# Flask demo application

Designed to demonstrate basic Python Flask application & run `pylint` over.

```bash
$ curl 0.0.0.0:5000/object/crayon
"Object crayon not found"

$ curl -X POST -d value=blue 0.0.0.0:5000/object/crayon
"Object crayon created successfully"

$ curl 0.0.0.0:5000/object/crayon
"blue"

$ curl -X DELETE 0.0.0.0:5000/object/crayon
"Object crayon deleted"

$ curl 0.0.0.0:5000/object/crayon
"Object crayon not found"
```
