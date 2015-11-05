from process_mux import SimplePmux, PmuxModule


class EchoModule1(PmuxModule):

    def __init__(self, endpoint):
        super(EchoModule1, self).__init__(endpoint, loopsleep=1)

    name = "echo_module_1"

    def _initial_state(self):
        return None


    def _iter(self, state, message):
        if message is None:
            print '[EchoModule1] no message..'
        else:
            print '[EchoModule1] received:', message
        return [('echo', "echo1")]


class EchoModule2(PmuxModule):

    def __init__(self, endpoint):
        super(EchoModule2, self).__init__(endpoint, loopsleep=1)

    name = "echo_module_2"

    def _initial_state(self):
        return None


    def _iter(self, state, message):
        if message is None:
            print '[EchoModule2] no message..'
        else:
            print '[EchoModule2] received:', message
        return [('echo', "echo2")]


class TestPmux(SimplePmux):

    def __init__(self):
        super(TestPmux, self).__init__(1)
        # modules
        # self._addPmuxModule(EchoModule1("derp"))
        # self._addPmuxModule(EchoModule2("herp"))
        self._addPmuxModule(EchoModule1("test1"))
        self._addPmuxModule(EchoModule2("test2"))
        # routes
        self.add_message_route('echo', EchoModule1, EchoModule2)
        self.add_message_route('echo', EchoModule2, EchoModule1)

t = TestPmux()
t.start()
