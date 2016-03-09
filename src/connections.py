"""Boundary object to abstract away communication layer."""
import nnpy
from abc import abstractmethod
from abc import ABCMeta


def create_nnpy_client_socket(connection_string):
    s = nnpy.Socket(nnpy.AF_SP, nnpy.REQ)
    s.connect(connection_string)
    return s


def create_nnpy_server_socket(connection_string):
    s = nnpy.Socket(nnpy.AF_SP, nnpy.REP)
    s.bind(connection_string)
    return s


class FrameworkConnection(object):
    """Boundary
    
    object for hiding connection complexity
    """

    __metaclass__ = ABCMeta

    def __init__(self, connection_string):
        self._conn = create_connection(connection_string)

    def send(self, data):
        self._conn.send(data)

    def recv(self):
        return self._conn.recv()

    @abstractmethod
    def create_connection(self, connection_string):
        pass


class FrameworkClientConnection(FrameworkConnection):
    def create_connection(self, connection_string):
        return create_nnpy_client_socket(connection_string)


class FrameworkServerConnection(FrameworkConnection):
    def create_connection(self, connection_string):
        return create_nnpy_server_socket(connection_string)


