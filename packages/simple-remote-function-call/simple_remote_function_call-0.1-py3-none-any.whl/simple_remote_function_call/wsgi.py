import flask
import pickle
import simple_remote_function_call as srfc
import os
from waitress import serve
import importlib
import importlib.util
import os.path


CURRENT_VERSION = "0.1"



app = flask.Flask(__name__)


imported = True
def pickled(func):
    return lambda *args, **kwargs: pickle.dumps(func(*args, **kwargs))

@app.route("/call", methods=['PUT'])
@pickled
def call():
    input = pickle.loads(flask.request.data)
    if input[0] != CURRENT_VERSION:
        return ("ERROR", Exception(f"Current Version {input[0]} does not match {CURRENT_VERSION}."))
    _, func_name, args, kwargs = input
    try:
        result = ("SUCCESS", srfc.GLOBAL.func_dict[func_name](*args, **kwargs))
    except Exception as ex:
        result = ("ERROR", ex)
    return result


@srfc.register
def hello_world(name="User"):
    return f"Hello {name}! You successfully executed a remote function call to hello_world!"

def start_server():
    with open("srfc.conf", "r") as f:
        alllines = f.read().split("\n")
    for line in alllines:
        module, func = line.split(":")
        path = os.path.join(os.getcwd(), module)
        spec = importlib.util.spec_from_file_location(module, f"{path}.py")
        imported = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported)
        srfc.register(getattr(imported, func))
    print(srfc.GLOBAL.func_dict)
    serve(app, host="0.0.0.0", port=8080)
