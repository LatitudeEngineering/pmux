from abc import ABCMeta
from functools import partial
from connections import NanomsgIpc


def execute(conn, function_name, *args, **kwargs):
    metadata = kwargs.get("metadata") or {}
    obj = {
        "function_name": function_name,
        "args": args,
        "metadata": metadata,
    }
    conn.send(obj)
    return conn.recv()
    

class SimpleClient(object):
    """Interactor

    Facilitates the client connection to the framework.
    """
    __metaclass__ = ABCMeta

    def __getattr__(self, name):
        #def to_execute(args=[], meta={}):
        #    return execute(self._conn, name, args, meta)
        #return to_execute
        return partial(execute, self._conn, name)
    

class SimpleIpc(SimpleClient):

    def __init__(self, id):
        self._conn = NanomsgIpc.create_client_socket(id) 

