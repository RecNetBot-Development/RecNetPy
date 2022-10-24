from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, List, Optional, TypeVar, TypedDict

if TYPE_CHECKING:
    from .. import Client
    from ..rest import RouteManager

RT = TypeVar("RT", bound=TypedDict)

class BaseDataClass(ABC, Generic[RT]):
    """
    The base class used for all dataclasses. This class is inteded to
    be inherited, and shouldn't be created directly.
    """

    id: int
    #: This is reference to the client that created the dataclass.
    client: 'Client'
    #: This is an interface for the HTTP manager.
    rec_net: 'RouteManager'
    #: Data returned by an API request.
    data: Optional[RT] = None

    def __init__(self, client: 'Client', id: int, data: Optional[RT] = None) -> None:
        self.client = client
        self.rec_net = client.rec_net
        self.id = id
        if data is not None: self.patch_data(data)

    @classmethod
    def create_from_id_list(cls, client: 'Client', ids: List[int]):
        """
        Creates a list of dataclasses from a list of ids.
        """
        dataclass_list: List[BaseDataClass] = []
        for id in ids:
            dataclass_obj = cls(client, id)
            dataclass_list.append(dataclass_obj)
        return dataclass_list

    @abstractmethod
    def patch_data(self, data: RT) -> None:
        pass