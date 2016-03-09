from abc import abstractmethod
from abc import ABCMeta


class Connection(object):
    """Interface for receiving connection"""

    def __init__(self, connection):
        self._conn = connection


class SourceConnection(Connection):
    """Interface for receiving connection"""

    def __init__(self, connection):
        super(SourceConnection, self).__init__(connection)

    def send(self, data):
        self._conn.send(data)


class SinkConnection(Connection):
    """Interface for sending connection"""

    def __init__(self, connection):
        super(SinkConnection, self).__init__(connection)

    def recv(self):
        return self._conn.recv()


class RemoteConnectionFactory(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_push_source((host, port)):
        pass

    @abstractmethod
    def create_pull_sink((host, port)):
        pass

    @abstractmethod
    def create_publish_source((host, port), topics=[]):
        pass

    @abstractmethod
    def create_subscribe_sink((host, port), topics=[]):
        pass


class IpcConnectionFactory(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_push_source(id):
        pass

    @abstractmethod
    def create_pull_sink(id):
        pass

    @abstractmethod
    def create_publish_source(id, topics=[]):
        pass

    @abstractmethod
    def create_subscribe_sink(id, topics=[]):
        pass

