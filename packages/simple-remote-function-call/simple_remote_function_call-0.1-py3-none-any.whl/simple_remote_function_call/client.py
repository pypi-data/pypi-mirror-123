import pickle
import http.client
CURRENT_VERSION = "0.1"


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def __getattr__(self, func_name):
        def call(*args, **kwargs):
            data = pickle.dumps((CURRENT_VERSION, func_name, args, kwargs))
            conn = http.client.HTTPConnection(self.host, self.port)
            conn.request("PUT","/call",data)
            response = conn.getresponse()
            r_data = response.read()
            unpickled = pickle.loads(r_data)
            status, result = unpickled
            if status == "ERROR":
                raise result
            elif status == "SUCCESS":
                return result
        return call