from abc import ABC
from typing import TypedDict

from .. import Client

class BaseManager(ABC):
    """
    The base class used by all managers.
    """
    def __init__(self, client: Client):
        self.client = client
        self.rec_net = client.rec_net