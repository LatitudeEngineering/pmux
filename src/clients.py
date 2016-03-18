from abc import ABCMeta
from connections import NanomsgIpc


class SimpleClient(object):
    """Interactor

    Facilitates the client connection to the framework.
    """
    __metaclass__ = ABCMeta

    def execute(self, function_name, args=[], metadata={}):
        obj = {
            "function_name": function_name,
            "args": args,
            "metadata": metadata,
        }
        self._conn.send(obj)
        return self._conn.recv()


class SimpleIpc(SimpleClient):

    def __init__(self, id):
        self._conn = NanomsgIpc.create_client_socket(id) 

