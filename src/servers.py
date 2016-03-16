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
        return self._lookup.items()

    def register(self, func):
        if not callable(func):
            raise NotCallableException("func must be callable.")
        self.function_lookup[func.__name__] = func

    def __call__(self, function_name, args):
        try:
            f = self.function_lookup[function_name]
            result = f(*args) 
        except Exception as e:
            print e
            traceback.print_exc()


