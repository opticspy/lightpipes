# -*- coding: utf-8 -*-
"""
Imitation of matlabs tic toc functions. Uses a stack and popping so that nested
timings can be done. Source:
https://stackoverflow.com/questions/5849800/tic-toc-functions-analog-in-python
Answer by user Stephan

Note: probably not thread safe

Created on Sun Jul 23 15:13:12 2017

@author: Lenny
"""

from time import time
_tstart_stack = []

def tic():
    """Start a new measurement by adding current time() to timing stack"""
    _tstart_stack.append(time())

def toc():
    """End the most recent measurement and return elapsed time in [s]"""
    return time() - _tstart_stack.pop()

def strtoc( prefix='', fmt=''):
    """End the most recent measurement and return elapsed time as string,
    given the format string"""
    if not fmt:
        fmt = "%.4ss"
    if prefix:
        return prefix + ': ' + fmt % toc() #add space if prefix set
    else:
        return fmt % toc()

def printtoc(prefix='', fmt=''):
    """End the most recent measurement and print the time to console given
    the format string"""
    print(strtoc(prefix, fmt))

def timeit(method):
    """Use as decorator for any function
    @timeit
    def myfunc(args):
        #do stuff
        return
    """
    """Inspired from
    https://medium.com/pythonhive/python-decorator-to-measure-the-execution
        -time-of-methods-fa04cb6bb36d
    """
    def timed(*args, **kw):
        tic()
        result = method(*args, **kw)
        printtoc(prefix='Time for '+method.__name__+': ')
        return result
    return timed

class printtimer:
    def __init__(self, prefix=''):
        """
        Generate a ContextManager to be used in the with statement.
        When the block enters, a timer is started with tictoc.tic()
        and when the block is left the timer is stopped and the elapsed
        time printed via tictoc.printtoc().
        Inside the `with` block all tic() calls must be matched with 
        a toc() otherwise the list of running timers will become corrupted.

        Parameters
        ----------
        prefix : str, optional
            Title/prefix to print with elapsed time. The default is ''.

        Returns
        -------
        Context Manager to be used in `with`.

        """
        self.prefix = prefix


    def __enter__(self):
        tic()


    def __exit__(self, extype, value, traceback):
        """If the block is exited normally, all 3 values will be None.
        If an exception occured, the values will contain the trace in the
        same format as returned by sys.exc_info()."""
        if extype is not None:
            self.prefix += ' (ended by Exception)'
        printtoc(self.prefix)





