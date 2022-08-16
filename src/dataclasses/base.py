from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, TypedDict

from .. import Client
from ..rest import APIRouteManager

RT = TypeVar("RT", bound=TypedDict)

class BaseDataClass(ABC, Generic[RT]):
    """
    The base class used for all dataclasses.
    """
    id: int
    client: Client
    rec_net: APIRouteManager

    def __init__(self, client: Client, id: int, data: Optional[RT] = None) -> None:
        self.client = client
        self.rec_net = client.rec_net
        self.id = id
        if data is not None: self.patch_data(data)

    @abstractmethod
    def patch_data(self, data: RT) -> None:
        pass