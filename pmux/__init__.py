from connections import LocalConnectionInfo
from connections import LocalConnectionFactory


def local_pair(string_id, perform_bind):
    info = LocalConnectionInfo(string_id)
    return LocalConnectionFactory.create_pair_connection(info, perform_bind)


def local_subscribe(string_id):
    info = LocalConnectionInfo(string_id)
    return LocalConnectionFactory.create_subscribe_sink(info)


def local_publish(string_id):
    info = LocalConnectionInfo(string_id)
    return LocalConnectionFactory.create_publish_source(info)

def local_push(string_id):
    info = LocalConnectionInfo(string_id)
    return LocalConnectionFactory.create_push_source(info)


def local_pull(string_id):
    info = LocalConnectionInfo(string_id)
    return LocalConnectionFactory.create_pull_sink(info)
