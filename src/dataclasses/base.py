from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar, TypedDict

from .. import Client
from ..rest import RouteManager

RT = TypeVar("RT", bound=TypedDict)

class BaseDataClass(ABC, Generic[RT]):
    """
    The base class used for all dataclasses.
    """
    id: int
    client: Client
    rec_net: RouteManager

    def __init__(self, client: Client, id: int, data: Optional[RT] = None) -> None:
        self.client = client
        self.rec_net = client.rec_net
        self.id = id
        if data is not None: self.patch_data(data)

    @classmethod
    def create_from_id_list(cls, client: Client, ids: List[int]):
        dataclass_list: List[BaseDataClass] = []
        for id in ids:
            dataclass_obj = cls(client, id)
            dataclass_list.append(dataclass_obj)
        return dataclass_list

    @abstractmethod
    def patch_data(self, data: RT) -> None:
        pass