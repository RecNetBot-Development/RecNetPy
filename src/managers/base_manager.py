from abc import ABC
from typing import Optional, TypedDict, Type

from .. import Client
from ..dataclasses import BaseDataClass

class BaseManager(ABC):
    """
    The base class used by all managers.
    """

    dataclass: Type[BaseDataClass]

    def __init__(self, client: Client):
        self.client = client
        self.rec_net = client.rec_net

    def create_dataclass(self, id: int, data: Optional[TypedDict] = None) -> BaseDataClass:
        """
        Creates an object from the managers corresponding dataclass.

        @param id: The unique number associated with each data response.
        @param data: The data from an API response associated with the dataclass.
        @return: Returns an object representing the data from the data response.
        """
        return self.dataclass(id, data)

    