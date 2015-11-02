# similar to pipeline, but using generic module class
from collections import defaultdict
from scholar.base.abstract_module import AbstractModule
import abc
import time


class PmuxModule(AbstractModule):
    """More strict implmentation of AbstractModule.

    """

    __metaclass__ = abc.ABCMeta

    #
    def __init__(self):
        super(PmuxModule, self).__init__()

    """Used by ProcessMux to route messages between PmuxModules"""
    name = 'change_me'

    ###########################
    ##  Abstract methods
    ###########################
    @abc.abstractmethod
    def _loop(self, message):
        """Work to be done in one interation"""
        pass
    @abc.abstractmethod
    def _cleanup(self):
        """Performs any necessary clean up actions in case execution ends prematurely"""
        pass


    ###########################
    ##  Implemented methods
    ###########################
    def startup_function(self, pipe):
        """Called when a new process is created with this object."""
        ## FOREVER
        try:
            while True:
                # prevent hotloop
                time.sleep(0.001)

                # message vars
                inMessage = None
                outMessages = []

                if pipe.poll():
                    inMessage = pipe.recv()
                # perform next iteration of work
                outMessages = self._loop(inMessage)
                if outMessages is not None:
                    for msg in outMessages:
                        pipe.send(msg)
                else:
                    pass
        except Exception as e:
            print e
        finally:
            # well, maybe not forever..
            pipe.close()
            self._cleanup()


    def loop(self, pipe):
        """Override AbstractModule's loop"""
        self.startup_function(pipe)


class ProcessMux(object):
    """
    This class attempts to abstract the functionality required for Pipeline.
    It mannages communication between processes via multiprocessing pipes
    Implementing this class requires overloading it's control and defineProcessMap
    methods.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, mainsleep=0.01):
        # stealing from travis
        self._startup = defaultdict(lambda: (None))
        self.defineProcessMap()
        # key value pair of (names, (obj, pipe)
        self._processes = defaultdict(lambda: (None, None))
        self._mainsleep = mainsleep

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
        (obj, pipe) = self._processes[pmux_module_type.name]
        pipe.send(message)

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
            pipe = obj.run()
            self._processes[key] = (obj, pipe)

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
            pipe = obj.restart()
            self._processes[key] = (obj, pipe)

    def mainloop(self):
        """
        This method checks for input for each element in self._process
        dictionary. When input is present self.control is envoked and
        passed contents of message.
        """
        msgCount = 0
        while True:
            # prevent hot loop
            if self._mainsleep !=0:
                time.sleep(self._mainsleep)

            pcs = self._processes
            # make sure all processes are running
            for key in pcs:
                self._ensureRunning(key)

            # check for input
            for key in pcs:
                #if self._processes[key].poll():
                (obj, pipe) = pcs[key]
                while pipe.poll() and msgCount < 10:
                    #print '[Worker]'
                    self._control(pipe.recv(), key)
                    msgCount += 1

                # reset counter
                msgCount = 0
