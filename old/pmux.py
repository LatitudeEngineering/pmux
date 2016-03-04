# similar to pipeline, but using generic module class
from collections import defaultdict
from multiprocessing import Process
import traceback
import zmq
import abc
import time


class AbstractModule(object):
    """
    This class defines an interface for objects to be used with
    pipeline class.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, endpoint):
        self._process = None
        self._endpoint = endpoint
        # previous non-zmq code
        # pipe = Pipe(True) # True = dual directional pipe
        # self.pipe = pipe[0] # pipe this module writes to
        # self._pipe = pipe[1] # pipe this module returns to caller


    def _runLoop(self, endpoint):
        # we are now in a new thread!
        # setup sockets
        ctx = zmq.Context()
        base_str = "ipc://%s_" % endpoint
        push = ctx.socket(zmq.PUSH)
        push.connect(base_str + "out")
        pull = ctx.socket(zmq.PULL)
        pull.connect(base_str + "in")

        # infinite loop
        self.loop((push, pull))

        push.close()
        pull.close()
        ctx.destroy()


    @abc.abstractmethod
    def loop(self, sockets):
        """
        Method to be implemented by extending class. Should be
        implemented with function that requires it's own process
        """
        pass


    def _reset(self):
        """
        Helper function to replace instance variables
        """
        # stop current process if running
        if self._process is None:
            pass
        elif self._process.is_alive():
            self._process.terminate()

        # reassing new process
        #self._process = Process(target=self._processMain)
        self._process = Process(target=self._runLoop, args=(self._endpoint,))


    def run(self):
        """
        Starts process with _processMain function.
        Returns port number.
        """
        # make sure not to start process multiple times
        if self._process is None:
            self._reset()
            self._process.start()
        elif not self._process.is_alive():
            #print 'process was dead. starting...'
            self._process.start()
        return self._endpoint


    def stop(self):
        """
        Resets all instance variables by calling private reset
        method. I chose to use reset because I don't want to
        worray about referencing null variables:)
        """
        self._reset()


    def isRunning(self):
        if not self._process.is_alive():
            return False
        return True


    def restart(self):
        """
        Destroys old pipe and process and then starts new process
        wit
        """
        # reset instance variables
        self._reset()
        # start again
        return self.run()


    # not working when del <obj> is called
    def __del__(self):
        """
        Overloading delete method so we can kill process in a
        responsible way.
        """
        # stop current process if running
        if self._process.is_alive():
            self._process.terminate()

        # self._pipe.close()
        # self.pipe.close()
        # calling super destructor
        super(AbstractModule, self).__delete__()


class PmuxModule(AbstractModule):
    """More strict implmentation of AbstractModule.

    """

    __metaclass__ = abc.ABCMeta

    #
    def __init__(self, endpoint, loopsleep = 0.01):
        self._sleepdur = loopsleep
        super(PmuxModule, self).__init__(endpoint)

    """Used by ProcessMux to route messages between PmuxModules"""
    name = 'change_me'

    ###########################
    ##  Abstract methods
    ###########################
    @abc.abstractmethod
    def _iter(self, state, message):
        """Work to be done in one interation"""
        pass


    @abc.abstractmethod
    def _initial_state(self):
        """Returns the initial state object that will continually be passed into _iter"""
        pass


    ###########################
    ##  Implemented methods
    ###########################
    def _cleanup(self):
        """Performs any necessary clean up actions in case execution ends prematurely"""
        return None


    def loop(self, sockets):
        """Called when a new process is created with this object."""
        ## FOREVER
        try:
            # vars
            push, pull = sockets
            state = self._initial_state()

            while True:
                # prevent hotloop
                time.sleep(self._sleepdur)

                # message vars
                inMessage = None
                outMessages = []

                val = pull.poll(10)
                #print '[PmuxModule] poll was:', val
                if val == 1:
                    inMessage = pull.recv_pyobj()
                    #print '[PmuxModule] received:', inMessage
                # perform next iteration of work
                try:
                    outMessages = self._iter(state, inMessage)
                    #print '[PmuxModule] outMessages:', outMessages
                except Exception as e:
                    print e
                    traceback.print_exc()
                if outMessages is not None:
                    for msg in outMessages:
                        #print '[PmuxModule] sending:', msg
                        push.send_pyobj(msg)
                        #print '[PmuxModule] done!'
                else:
                    pass
        except Exception as e:
            print e
            traceback.print_exc()
        finally:
            # well, maybe not forever..
            self._cleanup()


class ProcessMux(object):
    """
    This class attempts to abstract the functionality required for Pipeline.
    It mannages communication between processes via multiprocessing pipes
    Implementing this class requires overloading it's control and defineProcessMap
    methods.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, mainsleep=1):
        # stealing from travis
        self._startup = defaultdict(lambda: (None))
        self.defineProcessMap()
        # key value pair of (names, (obj, pipe)
        self._processes = defaultdict(lambda: (None, None))
        self._mainsleep = mainsleep
        self._ctx = zmq.Context()

    def _control(self, msg, sender_key):
        """
        Private method used to pass instance variables to implementing class.
        Not sure if this is necessare, but I think it makes for cleaner method
        implementation.
        """
        self.control(msg, sender_key, self._processes)

    @abc.abstractmethod
    def control(self, msg, sender_key, processes):
        """
        Method for mapping interprocess messages between modules. This method
        must be defined by the implementing class.
        """
        pass

    @abc.abstractmethod
    def defineProcessMap(self):
        """
        Called by __init__ to add modules to _processes dict to prepare for a
        subsequent call to run.
        """
        pass

    def _addProcessModule(self, name, module):
        """
        Given a module this method ensures it is of type ProcessMux and adds
        it to self._startup dict.
        """
        # ensure that module inherits from generic module
        if isinstance(module, AbstractModule):
            self._startup[name] = module
        else:
            print 'ERR: not generic module'

    def _addPmuxModule(self, pmux_module_instance):
        """Installs a pmux module into this instance of ProcessMux"""
        if isinstance(pmux_module_instance, PmuxModule):
            self._startup[pmux_module_instance.name] = pmux_module_instance
        else:
            raise Exception('pmux_module was not an instance of PmuxModule', pmux_module_instance)
        return None

    def _sendMessageToPmuxModule(self, message, pmux_module_type):
        (obj, socks) = self._processes[pmux_module_type.name]
        push, pull = socks
        push.send_pyobj(message)


    def __sock_helper(self, endpoint):
        #print 'binding sock..'
        base = "ipc://%s_" % endpoint
        push = self._ctx.socket(zmq.PUSH)
        pull = self._ctx.socket(zmq.PULL)
        push.bind(base + "in")
        pull.bind(base + "out")
        #print 'bound!', endpoint
        return (push, pull)


    def start(self):
        """
        Starts main execution thread and calls run method
        for every element in self._startup and adds it to
        self._process.
        """
        # uses reference and not deep copy so this is ok:)
        pcs = self._startup
        for key in pcs:
            # for each element, call run method to start background process
            # and add (element, pipe) tuple to self._process dict
            obj = pcs[key]
            port = obj.run()
            socks = self.__sock_helper(port)
            self._processes[key] = (obj, socks)

        # start main loop
        #print 'starting main loop'
        self.mainloop()

    def _ensureRunning(self, key):
        """
        Given a key this method ensures that it's corresponding
        process is running. If process is not already running
        this method restarts it via modules restart method.
        """

        (obj, pipe) = self._processes[key]
        # if object is not running then restart it and add it back to
        # self._processes dict
        if not obj.isRunning():
            #print 'wasn\'t running'
            endpoint = obj.restart()
            socks = self.__sock_helper(endpoint)
            self._processes[key] = (obj, socks)

    def mainloop(self):
        """
        This method checks for input for each element in self._process
        dictionary. When input is present self.control is envoked and
        passed contents of message.
        """
        while True:
            # prevent hot loop
            time.sleep(self._mainsleep)
            # print '---------------------------'
            # print 'ProcessMux'
            # print '---------------------------'

            pcs = self._processes
            # make sure all processes are running
            for key in pcs:
                self._ensureRunning(key)

            # check for input
            for key in pcs:
                #if self._processes[key].poll():
                (obj, socks) = pcs[key]
                push, pull = socks
                for i in range(10):
                    #print '[ProcessMux] polling socket..'
                    val = pull.poll(10)
                    #print '[ProcessMux] poll was', val
                    if val == 0:
                        #print '[ProcessMux] no messages'
                        break
                    msg = pull.recv_pyobj()
                    # print '[ProcessMux] msg from:', key
                    # print '[ProcessMux] received:', msg
                    self._control(msg, key)


class SimplePmux(ProcessMux):
    """Simplified abstraction of ProcessMux.
    """
    def __init__(self, mainsleep=0.1):
        self._routes = defaultdict(lambda: None)
        super(SimplePmux, self).__init__(mainsleep=mainsleep)


    # unused
    def defineProcessMap(self):
        pass


    def route_message(self, message, sender):
        """Routes message to the appropriate module.
            1) message[0], the message type
            2) sender, the source module's name
        """
        dest_module = self._routes[(sender, message[0])]
        if dest_module is None:
            err_str =   "---------------------------------------------"
            err_str +=  "[SimplePmux] UNHANDLED ROUTE"
            err_str +=  "[SimplePmux] sender:", sender
            err_str +=  "[SimplePmux] message:", message
            err_str +=  "---------------------------------------------"
            raise Exception(err_str)
        else:
            self._sendMessageToPmuxModule(message, dest_module)


    def add_message_route(self, message_type, src_module, dest_module):
        """Routes messages of message_type to dest_module when sent
        from src_module.
        """
        # print "[SimplePmux] adding route:"
        # print "[SimplePmux] message_type:", message_type
        # print "[SimplePmux] source module:", src_module.name
        # print "[SimplePmux] destination module:", dest_module.name
        entry = (src_module.name, message_type)
        self._routes[entry] = dest_module


    def control(self, message, sender, _):
        """Forwards relevant arguments to route_message"""
        self.route_message(message, sender)

