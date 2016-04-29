from pmux import PmuxNode
from factories import NanomsgIpc
from pmux import FunctionServer


class TestNode(PmuxNode):

    @property
    def name(self):
        return 'test_node'

    def _iteration(self, input_msg):
        print input_msg
        return 'testoutstring'

    def _cleanup(self):
        pass

def testfunc():
    source = NanomsgIpc.create_subscribe_source('test')
    # sink = NanomsgIpc.create_publish_sink('test')

    node = TestNode(source, None)
    node.run()


server = FunctionServer()

@server.register
def test1():
    return "test1 executed"

@server.register
def test2():
    return "test2 executed"

@server.register
def echo(to_echo):
    return to_echo

