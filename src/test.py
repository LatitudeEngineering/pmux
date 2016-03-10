from pmux import PmuxNode
from factories import NanomsgIpc

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

testfunc()
