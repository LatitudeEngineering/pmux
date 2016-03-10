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

    def recv(self):
        return self._conn.recv()


class SinkConnection(Connection):
    """Interface for sending connection"""

    def __init__(self, connection):
        super(SinkConnection, self).__init__(connection)

    def send(self, data):
        self._conn.send(data)


class ConnectionFactory(object):

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


