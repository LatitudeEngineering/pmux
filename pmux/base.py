from abc import abstractmethod
from abc import ABCMeta
from collections import namedtuple
from functools import partial


###############################################
##  Exceptions
###############################################
class MissingFunctionException(Exception):
    pass


class TimeoutException(Exception):
    pass


class ConnectionException(Exception):
    pass


class ConfigurationException(Exception):
    pass


class NotYetImplementedException(Exception):
    pass


class NotCallableException(Exception):
    pass


###############################################
##  serializer
###############################################
class Serializer(object):
    """Boundary interface handling serialization"""

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @staticmethod
    def serialize(obj):
        """consumes a python object and returns a string"""
        pass

    @staticmethod
    def deserialize(serialized):
        """consumes a string and returns a python object"""
        pass


###############################################
##  connection objects
###############################################
class PmuxConnection(object):
    """Interactor handling sending and receiving of data"""

    def __init__(self, connection, serializer):
        self._conn = connection
        self._ser = serializer
        self._poll = select.poll()
        self._poll.register(self._conn.getsockopt(nnpy.SOL_SOCKET, nnpy.RCVFD), select.POLLIN)

    def send(self, obj):
        str_data = self._ser.serialize(obj)
        self._conn.send(list(str_data))

    def recv(self):
        str_data = self._conn.recv()
        obj = self._ser.deserialize(str_data)
        return obj

    def close(self):
        self._conn.close()

    def poll(self):
        return self._conn.poll()


class PmuxSink(PmuxConnection):
    """Specifies send is unsupported"""

    def send(self, obj):
        raise ConfigurationException("PmuxSinks cannot send")


class PmuxSource(PmuxConnection):
    """Specifies recv is unsupported"""

    def recv(self):
        raise ConfigurationException("PmuxSources cannot recv")

    def poll(self):
        raise ConfigurationException("PmuxSources cannot poll")


RemoteConnectionInfo = namedtuple("TcpConnectionInfo", ["ip", "port"])
LocalConnectionInfo = namedtuple("IpcConnectionInfo", ["string_id"])


class PmuxConnectionFactory(object):
    """specifies connection creation functions"""
 
    @staticmethod
    def create_pair_connection(connection_info, bind_socket):
        pass
   
    @staticmethod
    def create_client_connection(connection_info):
        pass
    
    @staticmethod
    def create_server_connection(connection_info):
        pass
    
    @staticmethod
    def create_publish_source(connection_info):
        pass
    
    @staticmethod
    def create_subscribe_sink(connection_info):
        pass
    
    @staticmethod
    def create_push_source(connection_info):
        pass
    
    @staticmethod
    def create_pull_sink(connection_info):
        pass


###############################################
##  client related
###############################################
def execute(conn, function_name, *args, **kwargs):
    metadata = kwargs.get("metadata") or {}
    obj = {
        "function_name": function_name,
        "args": args,
        "metadata": metadata,
    }
    conn.send(obj)
    return conn.recv()
    

class FunctionClient(object):
    """Interactor

    Facilitates the client connection to the framework.
    """
    def __init__(self, client_connection):
        self._conn = client_connection

    def __getattr__(self, name):
        """allows client syntax as if functions were implemented locally"""
        return partial(execute, self._conn, name)


###############################################
##  server related
###############################################
class FunctionServer(object):
    """Entity
    
    Basic implementation of server.
    """
    def __init__(self):
        self._lookup = {}
        # add a hello world function for testing
        def hello_world():
            return "Hello from Python!"
        self._lookup['hello_world'] = hello_world

    def function_lookup(self):
        return self._lookup.items()

    def register(self, func):
        """adds func to the internal lookup"""
        if not callable(func):
            raise NotCallableException("func must be callable.")
        self._lookup[func.__name__] = func

    def __call__(self, function_name, args):
        """attempts to lookup function associated with function_name and calls it with args"""
        print "function_name: ", function_name
        print "args: ", args
        try:
            f = self._lookup[function_name]
            result = f(*args) 
            return result
        except Exception as e:
            print e
            traceback.print_exc()


###############################################
##  convenience objects
###############################################
class ComputationRequest(object):
    """Entity encapsulating computation to be executed.

    """
    def __init__(self, function_name_string, stdin_list, metadata_dict):
        self._fn = function_name_string
        self._in = stdin_list
        self._meta = metadata_dict

    @property
    def function_name(self):
        return self._fn

    @property
    def stdin(self):
        return tuple(self._in)

    @property
    def metadata(self):
        return self._meta


class ComputationResponse(object):
    """Entity encapsulating a function execution attempt.

    """
    def __init__(self, function_name_string, stdout_list, stderr_list, metadata_dict):
        self._fn = function_name_string
        self._out = stdout_list
        self._err = stderr_list
        self._meta = metadata_dict

    @property
    def function_name(self):
        return self._fn

    @property
    def stdout(self):
        return tuple(self._out)

    @property
    def stderr(self):
        return tuple(self._err)

    @property
    def metadata(self):
        return self._meta


class PmuxMessage(object):
    """Entity encapsulating a message within the pmux framework"""

    def __init__(self, message_name, **kwargs):
        self._name = message_name
        self._dict = kwargs
    
    @property
    def message_name(self):
        return self._name

    @property
    def message_values(self):
        return self._dict

