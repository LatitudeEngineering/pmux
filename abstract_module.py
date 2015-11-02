# attempting to make generic module for pipeline
import time
import abc
from multiprocessing import Pipe, Process

class AbstractModule(object):
    """
    This class defines an interface for objects to be used with
    pipeline class.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        #pipe = Pipe(False) # False = single directional pipe
        pipe = Pipe(True) # True = dual directional pipe
        self.pipe = pipe[0] # pipe this module writes to
        self._pipe = pipe[1] # pipe this module returns to caller
        #self._process = Process(target=self._processMain)
        self._process = Process(target=self._runLoop)

    def _runLoop(self):
        self.loop(self._pipe)

    @abc.abstractmethod
    def loop(self, pipe):
        """
        Method to be implemented by extending class. Should be
        implemented with function that requires it's own process
        """
        pass

    def _reset(self):
        """
        Helper function to replace instance variables
        """
        # close current pipe
        if self.pipe is not None:
            self.pipe.close()
            self._pipe.close()

        # reassign new pipe for reading and writing
        #(self.pipe, self._pipe) = Pipe(False)
        (self.pipe, self._pipe) = Pipe(True)

        # stop current process if running
        if self._process.is_alive():
            self._process.terminate()

        # reassing new process
        #self._process = Process(target=self._processMain)
        self._process = Process(target=self._runLoop)

    def run(self):
        """
        Starts process with _processMain function and returns
        readable pipe to caller
        """
        # make sure not to start process multiple times
        if not self._process.is_alive():
            self._process.start()

        return self.pipe

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
        if self._pipe.closed or self.pipe.closed:
            return False
        # might not need to check for none
        return True

    def restart(self):
        """
        Destroys old pipe and process. Then starts new process
        with new pipe.
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

        self._pipe.close()
        self.pipe.close()
        print 'stuff is done son!'
        # calling super destructor
        super(MessageModule, self).__delete__()
