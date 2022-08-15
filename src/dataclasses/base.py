
from abc import ABC, abstractstaticmethod
from typing import Optional, TypedDict

from .. import Client

class BaseDataClass(ABC):
    """
    The base class used for all dataclasses.
    """
    def __init__(self, client: Client, id: int, data: Optional[TypedDict] = None):
        self.client = client
        self.rec_net = client.rec_net
        self.id = id
        if data is not None: self.patch_data(data)

    @abstractstaticmethod
    def patch_data(self, data: TypedDict) -> None:
        pass