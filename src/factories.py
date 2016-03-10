from base import ConnectionFactory
from base import SourceConnection
from base import SinkConnection
import nnpy


ROOT_DIR = "/tmp/pmux_"

def bind_ipc_socket(id, nnpy_type):
    s = nnpy.Socket(nnpy.AF_SP, nnpy_type)
    ipc_str = "ipc://%s%s" % (ROOT_DIR, id)
    print ipc_str
    s.bind(ipc_str)
    return s


def connect_ipc_socket(id, nnpy_type):
    s = nnpy.Socket(nnpy.AF_SP, nnpy_type)
    ipc_str = "ipc://%s%s" % (ROOT_DIR, id)
    s.connect(ipc_str)
    return s


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
    return SourceConnection(s)


class NanomsgIpc(ConnectionFactory):

    @staticmethod
    def create_push_sink(id):
        s = bind_ipc_socket(id, nnpy.PUSH)
        return SinkConnection(s)

    @staticmethod
    def create_pull_source(id):
        s = connect_ipc_socket(id, nnpy.PULL)
        return SourceConnection(s)

    @staticmethod
    def create_publish_sink(id, topics=[]):
        s = bind_ipc_socket(id, nnpy.PUB)
        return SinkConnection(s)

    @staticmethod
    def create_subscribe_source(id, topics=[]):
        return nanomsg_subscribe_socket(id, topics, connect_ipc_socket)


class NanomsgRemote(ConnectionFactory):

    @staticmethod
    def create_push_sink((host, port)):
        s = bind_tcp_socket((host,port), nnpy.PUSH)
        return SinkConnection(s)

    @staticmethod
    def create_pull_source((host, port)):
        s = connect_tcp_socket((host, port), nnpy.PULL)
        return SourceConnection(s)

    @staticmethod
    def create_publish_sink((host, port), topics=[]):
        s = bind_tcp_socket((host,port), nnpy.PUB)
        return SinkConnection(s)

    @staticmethod
    def create_subscribe_source((host, port), topics=[]):
        return nanomsg_subscribe_socket((host,port), topics, connect_tcp_socket)
