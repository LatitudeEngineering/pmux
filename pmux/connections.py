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
            read_p = select.poll()
            read_fd = nnpy_socket.getsockopt(nnpy.SOL_SOCKET, nnpy.RCVFD)
            read_p.register(read_fd, select.POLLIN)
            def check_readable():
                return read_p.poll(0) != []
            self.check_readable = check_readable
        except:
            self.check_readable = None
        try:
            write_p = select.poll()
            write_fd = nnpy_socket.getsockopt(nnpy.SOL_SOCKET, nnpy.SNDFD)
            write_p.register(write_fd, select.POLLOUT)
            def check_writeable():
                return write_p.poll(0) != []
            self.check_writeable = check_writeable
        except:
            self.check_writeable = None


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
    def create_pair_connection(local_connection_info):
        ensure_localconnectioninfo(local_connection_info)
        bind_socket = local_connection_info.perform_bind
        create_function = bind_ipc_socket if bind_socket else connect_ipc_socket
        s = create_function(local_connection_info.string_id, nnpy.PAIR)
        return PmuxConnection(s, get_default_serializer())

    @staticmethod
    def create_client_connection(local_connection_info):
        ensure_localconnectioninfo(local_connection_info)
        bind_socket = local_connection_info.perform_bind
        create_function = bind_ipc_socket if bind_socket else connect_ipc_socket
        s = create_function(local_connection_info.string_id, nnpy.REQ)
        return PmuxConnection(s, get_default_serializer())

    @staticmethod
    def create_server_connection(local_connection_info):
        ensure_localconnectioninfo(local_connection_info)
        bind_socket = local_connection_info.perform_bind
        create_function = bind_ipc_socket if bind_socket else connect_ipc_socket
        s = create_function(local_connection_info.string_id, nnpy.REP)
        return PmuxConnection(s, get_default_serializer())

    @staticmethod
    def create_push_source(local_connection_info):
        ensure_localconnectioninfo(local_connection_info)
        bind_socket = local_connection_info.perform_bind
        create_function = bind_ipc_socket if bind_socket else connect_ipc_socket
        s = create_function(local_connection_info.string_id, nnpy.PUSH)
        return PmuxSource(s, get_default_serializer())

    @staticmethod
    def create_pull_sink(local_connection_info):
        ensure_localconnectioninfo(local_connection_info)
        bind_socket = local_connection_info.perform_bind
        create_function = bind_ipc_socket if bind_socket else connect_ipc_socket
        s = create_function(local_connection_info.string_id, nnpy.PULL)
        return PmuxSink(s, get_default_serializer())

    @staticmethod
    def create_publish_source(local_connection_info):
        ensure_localconnectioninfo(local_connection_info)
        bind_socket = local_connection_info.perform_bind
        create_function = bind_ipc_socket if bind_socket else connect_ipc_socket
        s = create_function(local_connection_info.string_id, nnpy.PUB)
        return PmuxSource(s, get_default_serializer())

    @staticmethod
    def create_subscribe_sink(local_connection_info):
        ensure_localconnectioninfo(local_connection_info)
        bind_socket = local_connection_info.perform_bind
        create_function = bind_ipc_socket if bind_socket else connect_ipc_socket
        s = nanomsg_subscribe_socket(local_connection_info.string_id, [], create_function)
        return PmuxSink(s, get_default_serializer())


def helper_remote(remote_connection_info, nnpy_sock_type):
    """helper for creating remote connections"""
    ensure_remoteconnectioninfo(remote_connection_info)
    bind_socket = remote_connection_info.perform_bind
    create_function = bind_tcp_socket if bind_socket else connect_tcp_socket
    s = create_function(remote_connection_info.string_id, nnpy_sock_type)
    return s 


class RemoteConnectionFactory(PmuxConnectionFactory):
    """constructs connections to remotes"""

    @staticmethod
    def create_pair_connection(remote_connection_info):
        s = helper_remote(remote_connection_info, nnpy.PAIR)
        return PmuxConnection(s, get_default_serializer())

    @staticmethod
    def create_client_connection(remote_connection_info):
        s = helper_remote(remote_connection_info, nnpy.REQ)
        return PmuxConnection(s, get_default_serializer())

    @staticmethod
    def create_server_connection(remote_connection_info):
        s = helper_remote(remote_connection_info, nnpy.REP)
        return PmuxConnection(s, get_default_serializer())

    @staticmethod
    def create_push_source(remote_connection_info):
        s = helper_remote(remote_connection_info, nnpy.PUSH)
        return PmuxSource(s, get_default_serializer())

    @staticmethod
    def create_pull_sink(remote_connection_info):
        s = helper_remote(remote_connection_info, nnpy.PULL)
        return PmuxSink(s, get_default_serializer())

    @staticmethod
    def create_publish_source(remote_connection_info):
        s = helper_remote(remote_connection_info, nnpy.PUB)
        return PmuxSource(s, get_default_serializer())

    @staticmethod
    def create_subscribe_sink(remote_connection_info):
        ensure_remoteconnectioninfo(remote_connection_info)
        bind_socket = remote_connection_info.perform_bind
        create_function = bind_tcp_socket if bind_socket else connect_tcp_socket
        s = nanomsg_subscribe_socket(remote_connection_info.string_id, [], create_function)
        return PmuxSink(s, get_default_serializer)

