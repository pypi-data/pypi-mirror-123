from __future__ import absolute_import
from taloncb.quotations import register_xpath_extensions
try:
    from taloncb import signature
    ML_ENABLED = True
except ImportError:
    ML_ENABLED = False


def init():
    register_xpath_extensions()
    if ML_ENABLED:
        signature.initialize()
