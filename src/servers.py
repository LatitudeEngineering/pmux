import abc


class FrameworkServer(object):
    """Interface for servers"""

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def function_lookup(self):
        pass

    @abc.abstractmethod
    def add_function(self, name, func):
        pass


class SimpleServer(FrameworkServer):
    """Entity
    
    Basic implementation of server.
    """
    def __init__(self):
        super(FrameworkServer, self).__init__()
        self._lookup = {}
        # add a hello world function for testing
        def hello_world():
            return "Hello from Python!"
        self._lookup['hello_world'] = hello_world

    def function_lookup(self):
        return self._lookup

    def add_function(self, name, func):
        if not callable(func):
            raise NotCallableException("func must be callable.")
        self.function_lookup[name] = func

    def __call__(self, function_name, args):
        try:
            f = self.function_lookup[function_name]
            result = f(*args) 
        except Exception as e:
            print e
            traceback.print_exc()


class ServerContext(object):
    """Interactor encapsulating Server, FrameworkConnection, and Serializer.
    
    """

    def __init__(self, server, framework_connection, serializer):
        self._server = server
        self._fc = framework_connection
        self._serializer = serializer

    def service():
        msg = self._fc.recv()
        print msg
        obj = self._serializer.deserialize(msg)


def create_server(local=None, remote=None):
    """Validates and returns Server handle
    Factory-ish function.
    """
    pass


def server_loop(server_obj, framework_connection):
    msg = fsc.recv()
    print msg


def try_serverloop(server_obj, framework_connection):
    try:
        server_loop(server_obj, framework_connection)
    except Exception as e:
        traceback.print_exc()


def run_server(server_context):
    s = Server()
    fsc = FrameworkServerConnection(CONN_STR)
    while True:
        # get message
        msg = fsc.recv()
        # do something with message
        print msg

