from process_mux import SimplePmux, PmuxModule


class EchoModule1(PmuxModule):

    def __init__(self, endpoint):
        super(EchoModule1, self).__init__(endpoint, loopsleep=1)

    name = "echo_module_1"

    def _loop(self, message):
        if message is None:
            return None
        print '[EchoModule] received:', message
        return [('echo', message + ",echo1")]

class EchoModule2(PmuxModule):

    def __init__(self, endpoint):
        super(EchoModule2, self).__init__(endpoint, loopsleep=1)

    name = "echo_module_2"

    def _loop(self, message):
        if message is None:
            print '[EchoModule2] sending echo2...'
            return [('echo',"echo2")]
        else:
            print '[EchoModule] received:', message
            return [('echo', message + ",echo2")]

class TestPmux(SimplePmux):

    def __init__(self):
        super(TestPmux, self).__init__()
        # modules
        self._addPmuxModule(EchoModule1("derp"))
        self._addPmuxModule(EchoModule2("herp"))
        # routes
        self.add_message_route('echo', EchoModule1, EchoModule2)
        self.add_message_route('echo', EchoModule2, EchoModule1)

t = TestPmux()
t.start()
