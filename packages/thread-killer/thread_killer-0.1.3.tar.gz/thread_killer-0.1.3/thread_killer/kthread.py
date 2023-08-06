import threading
import sys


class KillableThread(threading.Thread):
    """
    A subclass of threading.Thread, with a kill() method.
    The KThread class works by installing a trace in the thread. The trace checks at every line of execution whether
    it should terminate itself. So it's possible to instantly kill any actively executing Python code.
    """

    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        """installing a global trace in the thread."""
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        """installing a local trace in the thread."""
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        """Hacked killer function"""
        self.killed = True
