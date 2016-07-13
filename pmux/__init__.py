from connections import LocalConnectionInfo
from connections import LocalConnectionFactory
from connections import RemoteConnectionInfo
from connections import RemoteConnectionFactory


def local_pair(string_id, perform_bind):
    info = LocalConnectionInfo(string_id, perform_bind)
    return LocalConnectionFactory.create_pair_connection(info)


def local_subscribe(string_id):
    info = LocalConnectionInfo(string_id, False)
    return LocalConnectionFactory.create_subscribe_sink(info)


def local_publish(string_id):
    info = LocalConnectionInfo(string_id, True)
    return LocalConnectionFactory.create_publish_source(info)


def local_server(string_id):
    info = LocalConnectionInfo(string_id, True)
    return LocalConnectionFactory.create_server_connection(info)


def local_client(string_id):
    info = LocalConnectionInfo(string_id, False)
    return LocalConnectionFactory.create_client_connection(info)


def remote_server(ip, port):
    info = RemoteConnectionInfo(ip, port, True)
    return RemoteConnectionFactory.create_server_connection(info)


def remote_client(ip, port):
    info = RemoteConnectionInfo(ip, port, False)
    return RemoteConnectionFactory.create_client_connection(info)


def remote_publish(ip, port):
    info = RemoteConnectionInfo(ip, port, True)
    return RemoteConnectionFactory.create_publish_source(info)


def remote_subscribe(ip, port):
    info = RemoteConnectionInfo(ip, port, False)
    return RemoteConnectionFactory.create_subscribe_sink(info)

