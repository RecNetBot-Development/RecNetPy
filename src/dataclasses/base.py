
from abc import ABC, abstractstaticmethod

from .. import Client

class BaseDataClass(ABC):
    """
    The base class used for all dataclasses.
    """
    def __init__(self, client: Client, id: int):
        self.client = client
        self.rec_net = client.rec_net
        self.id = id

    @abstractstaticmethod
    def patch_data(self, data: dict) -> None:
        pass