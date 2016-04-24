from abc import abstractmethod
from abc import ABCMeta


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
##  connection objects
###############################################
class Connection(object):
    """Interface for receiving connection"""

    def __init__(self, connection):
        self._conn = connection


class SourceConnection(Connection):
    """Interface for receiving connection"""

    def __init__(self, connection):
        super(SourceConnection, self).__init__(connection)

    def recv(self):
        return self._conn.recv()


class SinkConnection(Connection):
    """Interface for sending connection"""

    def __init__(self, connection):
        super(SinkConnection, self).__init__(connection)

    def send(self, data):
        if not isinstance(data, str):
            raise Exception("data must be of type str")
        self._conn.send(list(data))


class ConnectionFactory(object):
    """Interface for constructing connections
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_push_sink((host, port)):
        pass

    @abstractmethod
    def create_pull_source((host, port)):
        pass

    @abstractmethod
    def create_publish_sink((host, port), topics=[]):
        pass

    @abstractmethod
    def create_subscribe_source((host, port), topics=[]):
        pass


###############################################
##  serializer
###############################################
class Serializer(object):
    """Boundary for serialization

    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def serialize(self, obj):
        pass

    @abc.abstractmethod
    def deserialize(self, serialized):
        pass


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

