import abc
import traceback


class FrameworkServer(object):
    """Interface for servers"""

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def function_lookup(self):
        pass

    @abc.abstractmethod
    def register(self, func):
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
        self._lookup[func.__name__] = func

    def __call__(self, function_name, args):
        print "function_name: ", function_name
        print "args: ", args
        try:
            f = self._lookup[function_name]
            result = f(*args) 
            return result
        except Exception as e:
            print e
            traceback.print_exc()


