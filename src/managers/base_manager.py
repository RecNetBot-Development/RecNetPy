from typing import Generic, Optional, TypeVar, TypedDict, Type

from .. import Client
from ..rest import APIRouteManager
from ..dataclasses import BaseDataClass

BDC = TypeVar("BDC", bound=BaseDataClass)
RT = TypeVar("RT", bound=TypedDict)

class BaseManager(Generic[BDC, RT]):
    """
    The base class used by all managers.
    """

    dataclass: BDC
    client: Client
    rec_net: APIRouteManager

    def __init__(self, client: Client):
        self.client = client
        self.rec_net = client.rec_net

    def create_dataclass(self, id: int, data: Optional[RT] = None) -> BDC:
        """
        Creates an object from the managers corresponding dataclass.

        @param id: The unique number associated with each data response.
        @param data: The data from an API response associated with the dataclass.
        @return: Returns an object representing the data from the data response.
        """
        return self.dataclass(self.client, id, data)

    