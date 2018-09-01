import time
import threading


class ParallelError(RuntimeError):
    """
    An parallel specfic runtime error
    """

class ParallelThread(object):
    """
    A parallel thread is an wrapper for Python's threading class which attempts
    to run each thread in parallel, yielding the process to allow the OS
    time to run another waiting parallel thread...
    """

    __slots__ = (
        '_target', '_args', '_kwargs', '_daemon', '_thread', '_terminated')

    def __init__(self, target=None, args=[], kwargs={}):
        if not callable(target):
            raise ParallelError('Target function not callable!')

        self._target = target
        self._args = args
        self._kwargs = kwargs

        self._daemon = True
        self._thread = None
        self._terminated = False

    def __repr__(self):
        return '<%s target=%s, args=%s, kwargs=%s, daemon=%s>' % (self.name,
            self._target, self._args, self._kwargs, self._daemon)

    @property
    def name(self):
        return '%s-%s' % (self.__class__.__name__, id(self))

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        if not callable(target):
            raise ParallelError('Target function not callable!')

        self._target = target

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args):
        self._args = args

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, kwargs):
        self._kwargs = kwargs

    @property
    def daemon(self):
        return self._daemon

    @daemon.setter
    def daemon(self, daemon):
        self._daemon = daemon

        if self._thread:
            self._thread.daemon = daemon

    @property
    def thread(self):
        return self._thread

    @thread.setter
    def thread(self, thread):
        self._thread = thread

    @property
    def terminated(self):
        return self._terminated

    @terminated.setter
    def terminated(self, terminated):
        self._terminated = terminated

    def start(self):
        if self._thread:
            raise ParallelError('Cannot start an already running thread %r!' % self)

        self._thread = threading.Thread(target=self.__run,
            args=self._args, kwargs=self._kwargs)

        self._thread.daemon = self._daemon
        self._thread.start()

    def __run(self):
        while not self._terminated:
            try:
                self._target(self, *self._args, **self._kwargs)
            except (KeyboardInterrupt, SystemExit):
                break

            consider_yield()

        self.shutdown()

    def shutdown(self):
        if not self._thread:
            raise ParallelError('Cannot shutdown an already shutdown thread!')

        if self._thread:
            self._thread.join()
            del self._thread

        self._target = None
        self._args = []
        self._kwargs = {}

        self._daemon = False
        self._thread = None
        self._terminated = False


def sleep():
    """
    Yield the process for a certain amount of time
    """

    time.sleep(0.0001)

def consider_yield():
    """
    Yield the process so another process can be ran
    """

    time.sleep(0)

def threaded(function):
    """
    A decorator for running a function within a thread
    """

    def decorator(*args, **kwargs):
        t = threading.Thread(target=function,
            args=args, kwargs=kwargs)

        t.daemon = True
        t.start()

        return t

    return decorator

def parallel_threaded(function):
    """
    A decorator for running a function within a parallel thread
    """

    def decorator(*args, **kwargs):
        t = ParallelThread(target=function,
            args=args, kwargs=kwargs)

        t.daemon = True
        t.start()

        return t

    return decorator

def locked(function):
    """
    A decorator for running a function within a mutex lock
    """

    def decorator(*args, **kwargs):
        lock = threading.Lock()
        lock.acquire()

        try:
            result = function(*args, **kwargs)
        finally:
            lock.release()

        del lock
        return result

    return decorator
