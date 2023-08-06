"""
    gitdata
"""

from .utils import Record
from .stores.records import table_of
from .stores.entities import store_of
from .__version__ import __version__
from .connectors.http import HttpConnector

def fetch(ref):
    """Fetch data

    Stub for fetch data function.
    """
    return Record(HttpConnector().get(ref))
