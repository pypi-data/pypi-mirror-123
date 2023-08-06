__version__ = '0.3.6'
VERSION = __version__.split('.')

def version(split=False):
    return __version__ if not split else VERSION
