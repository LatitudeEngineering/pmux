from abc import abstractmethod
from abc import ABCMeta
from base import RemoteConnectionInfo
from base import LocalConnectionInfo
from base import PmuxConnection
from base import PmuxSink
from base import PmuxSource
from base import PmuxConnectionFactory
from serializers import get_default_serializer
import select
# message queue library
import nnpy
# directory where pmux file descriptors are stored
ROOT_DIR = "/tmp/pmux_"


class ConnectionWrap(object):
    """convenient wrapper for nnpy sockets"""
    def __init__(self, nnpy_socket):
        self.send = nnpy_socket.send
        self.recv = nnpy_socket.recv
        self.close = nnpy_socket.close
        self.setsockopt = nnpy_socket.setsockopt
        self.getsockopt = nnpy_socket.getsockopt
        # construct poll function
        try:
            p = select.poll()
            fd = nnpy_socket.getsockopt(nnpy.SOL_SOCKET, nnpy.RCVFD)
            p.register(fd, select.POLLIN)
            def poll():
                return p.poll(0) != []
            self.poll = poll
        except:
            print "poll function not set up"

def bind_ipc_socket(id, nnpy_type):
    s = nnpy.Socket(nnpy.AF_SP, nnpy_type)
    ipc_str = "ipc://%s%s" % (ROOT_DIR, id)
    s.bind(ipc_str)
    return ConnectionWrap(s)


def connect_ipc_socket(id, nnpy_type):
    s = nnpy.Socket(nnpy.AF_SP, nnpy_type)
    ipc_str = "ipc://%s%s" % (ROOT_DIR, id)
    s.connect(ipc_str)
    return ConnectionWrap(s)


def bind_tcp_socket((host,port), nnpy_type):
    s = nnpy.Socket(nnpy.AF_SP, nnpy_type)
    tcp_str = "tcp://%s:%s" % (host, port)
    s.bind(tcp_str)
    return s


def connect_tcp_socket((host,port), nnpy_type):
    s = nnpy.Socket(nnpy.AF_SP, nnpy_type)
    tcp_str = "tcp://%s:%s" % (host, port)
    s.connect(tcp_str)
    return s


def nanomsg_subscribe_socket(connection_details, topics, socket_func):
    if type(topics) is not list:
        raise Exception("topics must be a list")
    s = socket_func(connection_details, nnpy.SUB)
    if topics == []:
        s.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, '')
    else:
        for topic in topics:
            s.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, topic)
    return s


def ensure_localconnectioninfo(obj):
    if not isinstance(obj, LocalConnectionInfo):
        raise ConfigurationException("obj must be LocalConnectionInfo")
    return None


def ensure_remoteconnectioninfo(obj):
    if not isinstance(obj, RemoteConnectionInfo):
        raise ConfigurationException("obj must be RemoteConnectionInfo")
    return None


class LocalConnectionFactory(PmuxConnectionFactory):
    """constructs connections used on the local device

    """
    
    @staticmethod
    def create_pair_connection(local_connection_info, bind_socket):
        ensure_localconnectioninfo(local_connection_info)
        create_function = bind_ipc_socket if bind_socket else connect_ipc_socket
        s = create_function(local_connection_info.string_id, nnpy.PAIR)
        return PmuxConnection(s, get_default_serializer())

    @staticmethod
    def create_client_connection(local_connection_info):
        ensure_localconnectioninfo(local_connection_info)
        s = connect_ipc_socket(local_connection_info.string_id, nnpy.REQ)
        return PmuxConnection(s, get_default_serializer())

    @staticmethod
    def create_server_connection(local_connection_info):
        ensure_localconnectioninfo(local_connection_info)
        s = bind_ipc_socket(local_connection_info.string_id, nnpy.REP)
        return PmuxConnection(s, get_default_serializer())

    @staticmethod
    def create_push_source(local_connection_info):
        ensure_localconnectioninfo(local_connection_info)
        s = bind_ipc_socket(local_connection_info.string_id, nnpy.PUSH)
        return PmuxSource(s, get_default_serializer())

    @staticmethod
    def create_pull_sink(local_connection_info):
        ensure_localconnectioninfo(local_connection_info)
        s = connect_ipc_socket(local_connection_info.string_id, nnpy.PULL)
        return PmuxSink(s, get_default_serializer())

    @staticmethod
    def create_publish_source(local_connection_info):
        ensure_localconnectioninfo(local_connection_info)
        s = bind_ipc_socket(local_connection_info.string_id, nnpy.PUB)
        return PmuxSource(s, get_default_serializer())

    @staticmethod
    def create_subscribe_sink(local_connection_info):
        ensure_localconnectioninfo(local_connection_info)
        s = nanomsg_subscribe_socket(local_connection_info.string_id, [], connect_ipc_socket)
        return PmuxSink(s, get_default_serializer())

