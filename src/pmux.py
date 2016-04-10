import traceback
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from connections import NanomsgIpc
from serializers import MsgpackSerializer
from servers import SimpleServer


class PmuxNode(object):
    """Base uMux object implementing general structure of processing.

    """

    __metaclass__ = ABCMeta


    def __init__(   self,
                    source_connection=None,
                    sink_connection=None,
                    serializer=MsgpackSerializer()):
        self._source = source_connection
        self._sink = sink_connection
        self._serializer = serializer

    @abstractproperty
    def name(self):
        pass

    @abstractmethod
    def _iteration(self, input_message):
        pass

    @abstractmethod
    def _cleanup(self):
        pass

    def _loop(self, input_message):
        output_messages = []
        try:
            output_messages = self._iteration(input_message)
        except Exception as e:
            print "[uMuxNode-"+self.name+"] error: ", e
            traceback.print_exc()
        return output_messages

    def _main(self):
        while True:
            input_message = None
            output_messages = None
            if self._source is not None:
                packed = self._source.recv()
                input_message = self._serializer.deserialize(packed)
            output_messages = self._loop(input_message)
            if self._sink is not None:
                for msg in output_messages:
                    to_send = self._serializer.serialize(msg)
                    self._sink.send(list(to_send))

    def run(self):
        try:
            self._main()
        except:
            traceback.print_exc()
        finally:
            self._cleanup()


def infinite_loop(connection, server):
    while True:
        msg = connection.recv()
        function_name = msg["function_name"]
        args = msg["args"]
        try:
            output = server(function_name, args)
            connection.send(output)
        except:
            traceback.print_exc()


def run(connection, server):
    try:
        infinite_loop(connection, server)
    except:
        traceback.print_exc()
    finally:
        connection.close()


class FunctionServer(object):
    """Handles executing functions for some remote client"""
    def __init__(self):
        self._server = SimpleServer()

    def register(self, func):
        self._server.register(func)
        return func

    def run_local(self, id):
        conn = NanomsgIpc.create_server_socket(id)
        run(conn, self._server)

    def run_remote(self, port):
        raise Exception("Not implemented yet.")

