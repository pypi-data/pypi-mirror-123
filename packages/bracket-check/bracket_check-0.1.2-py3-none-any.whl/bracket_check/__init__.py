import sys

from bracket_check.app import bracket_checker

__version__ = '0.1.2'

class CallableModule:
    """A class that makes the module callable."""

    def __init__(self, wrapped):
        self._wrapped = wrapped

    def __call__(self, *args, **kwargs):
        return self._wrapped.main(*args, **kwargs)

    def __getattr__(self, attr):
        return object.__getattribute__(self._wrapped, attr)


sys.modules[__name__] = CallableModule(sys.modules[__name__])


def main(*args, **kwargs):
    return bracket_checker(*args, **kwargs)
