class SimpleClient(object):
    """Interactor

    Facilitates the client connection to the framework.
    """
    def __init__(self, framework_connection):
        self._conn = framework_connection
    def execute(self, args):
        self._conn.send(args)
        return self._conn.recv()


def validate_local_configuration(string_id):
    pass


def validate_remote_configuration(host, port):
    pass


def create_remote_simpleclient(host, port):
    pass


def create_local_simpleclient(string_id):
    pass


def connect_to_local_server(string_id):
    validate_local_configuration(string_id)
    return create_local_simpleclient(connection_string)


def connect_to_remote_server(host, port):
    validate_remote_configuration(host, port)
    return create_remote_simpleclient(host, port)
