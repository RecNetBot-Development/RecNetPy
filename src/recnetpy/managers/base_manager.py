from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, List, Optional, TypeVar, TypedDict, Type

if TYPE_CHECKING:
    from .. import Client
    from ..rest import RouteManager
    from ..dataclasses import BaseDataClass


BDC = TypeVar("BDC", bound='BaseDataClass')
RT = TypeVar("RT", bound=TypedDict)

class BaseManager(ABC, Generic[BDC, RT]):
    """
    The base class used by all managers. This class 
    is only to be inherited, and shouldn't be created
    manually.
    """

    #: This is the dataclass the manager is responsible for creating.
    dataclass: Type[BDC]
    #: This is a reference to the main client interface.
    client: 'Client'
    #: This is an interface for the HTTP manager.
    rec_net: 'RouteManager'

    def __init__(self, client: 'Client'):
        self.client = client
        self.rec_net = client.rec_net

    @abstractmethod
    async def fetch(self, id: int) -> BDC:
        """
        Fetches the data for an object by its id, and returns
        the class representing the data.

        :param id: The unique number associated with each data response.
        :retun: Returns an object representing the data from the data response.
        """
        pass

    @abstractmethod
    def create_dataclass(self, id: int, data: Optional[RT] = None) -> BDC:
        """
        Creates an object from the managers corresponding dataclass.

        :param id: The unique number associated with each data response.
        :param data: The data from an API response associated with the dataclass.
        :return: Returns an object representing the data from the data response.
        """
        pass

    @abstractmethod
    def create_from_data_list(self, data: List[RT]) -> List[BDC]:
        """
        Creates a list of objects from a list of data.

        :param data: A list of data from an API response associated with the dataclass.
        :return: A list of objects.
        """
        pass
    